import pygame
import pygame.sprite

from shape import Shape

def check_keydown_events(event, game_settings, shape, squares, mix):
    if event.key == pygame.K_ESCAPE:
        pygame.quit()
    if game_settings.game_active:
        if event.key == pygame.K_DOWN:
            shape.speed_up = True
        elif event.key == pygame.K_RIGHT:
            shape.move_right()
            # Check if moved into already place blocks; undo if so
            collisions = check_collisions(shape, squares)
            if collisions:
                shape.move_left()
        elif event.key == pygame.K_LEFT:
            shape.move_left()
            # Check if moved into already place blocks; undo if so
            collisions = check_collisions(shape, squares)
            if collisions:
                shape.move_right()
        elif event.key == pygame.K_UP:
            mix.play_rotate()
            shape.rotate_shape()


def check_keyup_events(event, shape):
    if event.key == pygame.K_DOWN:
        shape.speed_up = False


def check_events(game_settings, shape, squares, sb, mix):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, shape, squares, mix)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, shape)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Start a new game when player clicks "New Game"
            clicked = sb.button_rect.collidepoint(mouse_x, mouse_y)
            if clicked:
                start_game(game_settings, shape, squares, sb)


def check_collisions(shape, squares):
    # The pile is all squares that are not a part of the current shape
    pile = [square for square in squares.sprites() if not square.a_part]
    return pygame.sprite.groupcollide(shape.parts, pile, False, False)


def check_shape(shape, play_area, squares, game_settings, sb, mix):
    # Checks if shape reached the bottom; creates a new one if so
    collisions = check_collisions(shape, squares)
    for part in shape.parts:
        if part.rect.bottom >= play_area.rect.bottom or collisions:
            mix.play_landed()
            for part in shape.parts:
                part.a_part = False
            # Check if shape didn't move after spawning; stop the game if so
            spawn_point = play_area.rect.top + game_settings.square_size * 2
            if shape.parts[0].rect.top <= spawn_point + 5:
                mix.play_lost()
                game_settings.game_active = False
                break
            shape.parts.clear()
            # Check if any rows were filled. Twice, because first check may fill more rows
            check_rows(play_area, squares, game_settings, sb)
            check_rows(play_area, squares, game_settings, sb)
            # Make a new shape
            shape.make_shape(squares)
            break


def check_rows(play_area, squares, game_settings, sb):
    # Checks if there is enough squares around the same Y-coordinate.
    # If yes, deletes them and moves the squares above lower
    rows = [(play_area.rect.bottom - (game_settings.square_size / 2 +
                                      num * game_settings.square_size)) for num in range(10)]
    deleted = []
    for row in rows:
        counter = [square for square in squares.sprites() if row - 10 < square.rect.centery < row + 10]
        if len(counter) == play_area.rect.width / game_settings.square_size:
            for square in counter:
                square.kill()
            deleted.append(row)

    # Check if any rows were deleted; if so - move everything above them lower
    for row in reversed(deleted): # Checking from the end means checking from top to bottom
        above = [sq for sq in squares.sprites() if sq.rect.centery < row + 5]
        for sq in above:
            sq.rect.centery += game_settings.square_size

    # Update score
    sb.score += len(deleted) * len(deleted) * 10
    sb.prep_score()

    # Drop down any square that has nothing below it; drop all squares above that one too
    if deleted:
        dropped = []
        for square in squares.sprites():
            below = [sq for sq in squares.sprites() if sq.rect.x == square.rect.x and sq.rect.y > square.rect.y + 5]
            if not below:
                square.rect.centery = rows[0]
                dropped.append(square)
        for square in dropped:
            above = [sq for sq in squares.sprites() if sq.rect.x == square.rect.x and sq.rect.y < square.rect.y - 5]
            for i, sq in enumerate(above):
                sq.rect.centery = rows[i+1]


def start_game(game_settings, shape, squares, sb):
    # Delete all squares, update scores, create new shape, and make the game active
    if sb.score > int(sb.top_score):
        with open('top_score.txt', 'w') as file:
            file.write(str(sb.score))
    sb.prep_top_score()
    sb.score = 0
    sb.prep_score()
    squares.empty()
    shape.make_shape(squares)
    game_settings.game_active = True


def update_screen(screen, game_settings, sb, play_area, squares, shape):
    screen_rect = screen.get_rect()
    screen.blit(game_settings.bg_image, screen_rect)

    if game_settings.game_active:
        shape.update_shape()
    for square in squares.sprites():
        square.draw_square()

    play_area.show_area()
    sb.show_stuff()

    pygame.display.flip()
