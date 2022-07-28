import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Alien control class"""
    def __init__(self, ai_game):
        """Initialize an alien & set its initial position"""
        super().__init__()
        self.screen = ai_game.screen

        # Load alien image
        self.image = pygame.image.load("images/alien_ship.bmp")
        self.rect = self.image.get_rect()

        # Set initial alien position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Save x-coordinate of the alien ship
        self.x = float(self.rect.x)