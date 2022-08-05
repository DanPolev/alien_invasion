import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for control bullet that ship fired"""

    def __init__(self, ai_game):
        """Create bullets at current ship position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Create a bullet
        self.image = pygame.image.load("images/bullet.bmp")
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        # TODO: only for debugging
        # self.rect.w = 3000

        # Bullet position is stored in float format
        self.y = float(self.rect.y)

    def update(self):
        """Move a bullet up the screen"""
        # Update bullet position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

        if self.rect.bottom <= self.screen_rect.top:
            self.kill()
