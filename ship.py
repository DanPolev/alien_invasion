import pygame

class Ship():
    """Ship control class"""

    def __init__(self, ai_game):
        """Initialize the ship, set its initial position"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Load spaceship image, get rectangle
        self.image = pygame.image.load("images/spaceship.bmp")
        self.rect = self.image.get_rect()

        # Set initial ship position
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship in current position"""
        self.screen.blit(self.image, self.rect)