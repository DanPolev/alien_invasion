import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for control bullet that ship fired"""

    def __init__(self, ai_game):
        """Create bullets at current ship position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a bullet at (0,0) position, then assign true current position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Bullet position is stored in float format
        self.y = float(self.rect.y)

    def update(self):
        """Move a bullet up the screen"""
        # Update bullet position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        """Draw a bullet on the screen"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
