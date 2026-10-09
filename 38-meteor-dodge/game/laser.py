import pygame


class Laser:
    SPEED = 10
    WIDTH = 4
    LENGTH = 14

    def __init__(self, x, y):
        self.rect = pygame.Rect(x - self.WIDTH // 2, y - self.LENGTH, self.WIDTH, self.LENGTH)

    def update(self):
        self.rect.y -= self.SPEED

    def off_screen(self):
        return self.rect.bottom < 0

    def hits(self, meteor):
        # circle (meteor) vs rect (laser): clamp meteor centre to the rect
        px = max(self.rect.left, min(meteor.x, self.rect.right))
        py = max(self.rect.top, min(meteor.y, self.rect.bottom))
        return (meteor.x - px) ** 2 + (meteor.y - py) ** 2 <= meteor.radius ** 2

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 80, 80), self.rect)
        core = self.rect.inflate(-2, 0)
        pygame.draw.rect(screen, (255, 230, 230), core)
