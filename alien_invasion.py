import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion by DanPolev")

        self.ship = Ship(self)
        self.bg_image = pygame.image.load("images/space_background.bmp")
        self.bullets = pygame.sprite.Group()

    def blit_bg_image(self):
        """Blit background image on the screen"""
        self.screen.blit(self.bg_image, self.screen_rect)

    def _check_events(self):
        """Process keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        """Process keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """Process keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _fire(self):
        """Make new bullet & add it to the bullets group"""
        if len(self.bullets) < self.settings.max_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update screen state"""
        # Update background
        self.blit_bg_image()
        # Update ship state
        self.ship.blitme()
        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw()
        # Display last drawn screen
        pygame.display.flip()

    def delete_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def run_game(self):
        """Run main loop"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self.delete_bullets()
            self._update_screen()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()