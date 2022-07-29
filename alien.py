import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Alien control class"""
    def __init__(self, ai_game):
        """Initialize an alien & set its initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image
        self.image = pygame.image.load("images/alien_ship.bmp")
        self.rect = self.image.get_rect()

        # Set initial alien position
        self.rect.x = self.rect.w
        self.rect.y = self.rect.h

        # Save x-coordinate of the alien ship
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien's reached the screen edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move alien right/left"""
        self.x += self.settings.alien_speed * self.settings.fleet_dir
        self.rect.x = self.x