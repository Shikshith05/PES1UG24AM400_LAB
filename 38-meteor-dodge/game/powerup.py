import math
import random
import pygame


class ShieldOrb:
    """Drifting energy orb. Collect it to get a one-hit shield."""

    def __init__(self, width):
        self.base_x = random.randint(40, width - 40)
        self.x = self.base_x
        self.y = -20
        self.vy = 1.6
        self.radius = 13
        self.t = random.uniform(0, 6.28)

    def update(self):
        self.t += 0.06
        self.y += self.vy
        self.x = self.base_x + math.sin(self.t) * 30  # gentle sideways drift

    def off_screen(self, height):
        return self.y > height + 40

    def collides(self, rect):
        dx, dy = self.x - rect.centerx, self.y - rect.centery
        return (dx * dx + dy * dy) ** 0.5 < self.radius + 18

    def draw(self, screen):
        pulse = 2 * math.sin(self.t * 3)
        x, y = int(self.x), int(self.y)
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(glow, (80, 220, 255, 60), (40, 40), int(24 + pulse))
        screen.blit(glow, (x - 40, y - 40))
        pygame.draw.circle(screen, (60, 200, 255), (x, y), self.radius)
        pygame.draw.circle(screen, (200, 250, 255), (x, y), self.radius - 5)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), self.radius, 2)