import pygame


class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, color):
        self.game = game
        self.pos = pos
        self.size = size 
        self.color = color
        self.velocity = [0,0]
        self.display = pygame.surface.Surface(self.size)
        self.velocity = [0,0]

    def update(self, movement, offset=[0,0]):
        self.pos[0]+= movement[0]
        self.pos[1]+= movement[1]
    def rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    def render(self, surf, offset = (0,0)):
        self.display.fill(self.color)
        rect = self.rect()
        surf.blit(self.display, (rect[0] - offset[0], rect[1] - offset[1]))
