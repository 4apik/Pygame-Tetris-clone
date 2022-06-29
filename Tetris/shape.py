from random import randint, choice

from square import Square

class Shape:
    def __init__(self, screen, play_area, game_settings):
        self.screen = screen
        self.play_area = play_area
        self.area_rect = play_area.rect
        self.game_settings = game_settings

        self.speed_up = False

    def make_shape(self, squares):
        # Create squares to make a shape out of
        self.color = (randint(50, 200), randint(50, 200), randint(50, 200))
        self.parts = [Square(self.game_settings, self.screen, self.color) for _ in range(4)]

        # Place these squares correctly
        # Place the first one in the middle, at the top of play area
        self.parts[0].rect.centerx = self.area_rect.centerx + self.game_settings.square_size/2
        self.parts[0].rect.top = self.area_rect.top + self.game_settings.square_size * 2

        # Attach the rest of them to each other randomly
        for i in range(3):
            # choose from already placed ones
            old = choice(self.parts[:i+1]) # <- random.choice()
            self.check_empty(old)
            # choose from not placed ones
            new = self.parts[i+1]
            to = choice(self.choices) # <- random.choice()
            self.attach(to, new, old)

        for part in self.parts:
            squares.add(part)

    def check_empty(self, old):
        # Checks which sides are still available for attachments
        self.choices = ['top', 'bottom', 'left', 'right']
        for part in self.parts:
            if part.rect.centerx == old.rect.centerx:
                if part.rect.top == old.rect.bottom:
                    self.choices.remove('bottom')
                elif part.rect.bottom == old.rect.top:
                    self.choices.remove('top')
            elif part.rect.centery == old.rect.centery:
                if part.rect.left == old.rect.right:
                    self.choices.remove('right')
                elif part.rect.right == old.rect.left:
                    self.choices.remove('left')

    def attach(self, to, new, old):
        funcs = {'top': self.attach_to_top, 'bottom': self.attach_to_bottom,
                 'left': self.attach_to_left, 'right': self.attach_to_right}
        chosen = funcs.get(to)
        chosen(new, old)

    def attach_to_top(self, new, old):
        new.rect.centerx = old.rect.centerx
        new.rect.bottom = old.rect.top
        new.connections.append((old, 'bottom'))

    def attach_to_bottom(self, new, old):
        new.rect.centerx = old.rect.centerx
        new.rect.top = old.rect.bottom
        new.connections.append((old, 'top'))

    def attach_to_left(self, new, old):
        new.rect.centery = old.rect.centery
        new.rect.right = old.rect.left
        new.connections.append((old, 'right'))

    def attach_to_right(self, new, old):
        new.rect.centery = old.rect.centery
        new.rect.left = old.rect.right
        new.connections.append((old, 'left'))

    def update_shape(self):
        for square in self.parts:
            if self.speed_up:
                square.rect.y += self.game_settings.shape_speed * 3
            else:
                square.rect.y += self.game_settings.shape_speed

    def move_right(self):
        # Check if all of the parts are not next to the right side
        can = [part for part in self.parts if part.rect.right < self.area_rect.right]
        if len(can) == 4:
            for part in self. parts:
                part.rect.x += self.game_settings.square_size

    def move_left(self):
        # Check if all of the parts are not next to the left side
        can = [part for part in self.parts if part.rect.left > self.area_rect.left]
        if len(can) == 4:
            for part in self.parts:
                part.rect.x -= self.game_settings.square_size

    def rotate_shape(self):
        self.sides = ['top', 'left', 'bottom', 'right']
        for part in self.parts[1:]:
            for conn in part.connections:
                new_side = self.sides[(self.sides.index(conn[1]) + 1) % 4] # works
                square = conn[0]
                self.attach(new_side, part, square)
                part.connections.pop(0)
        for part in self.parts:
            if part.rect.centerx > self.area_rect.right:
                self.move_left()
            elif part.rect.centerx < self.area_rect.left:
                self.move_right()
