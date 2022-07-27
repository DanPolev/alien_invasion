import pygame

class Ship():
    """Ship control class"""

    def __init__(self, ai_game):
        """Initialize the ship, set its initial position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings

        # Load spaceship image, get rectangle
        self.image = pygame.image.load("images/spaceship.bmp")
        self.rect = self.image.get_rect()

        # Set initial ship position
        self.rect.midbottom = self.screen_rect.midbottom

        # x-coordinate
        self.x = float(self.rect.x)

        # Moving flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship in current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Check moving flag, move the ship until flag is False"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
