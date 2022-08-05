import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion


class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion by DanPolev")

        self.ship = Ship(self)
        self.bg_image = pygame.image.load("images/space_background.bmp")
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """Create alien fleet"""
        alien = Alien(self)
        avail_space_x = self.screen_rect.w - 2 * alien.rect.w
        avail_space_y = self.screen_rect.h - 2 * alien.rect.h -self.ship.rect.h
        number_aliens_x = avail_space_x // (2 * alien.rect.w)
        number_aliens_y = avail_space_y // (2 * alien.rect.h)

        for row in range(number_aliens_y):
            for col in range(number_aliens_x):
                self._create_alien(row, col)

    def _create_alien(self, row, col):
        """Create an alien for the given row & column id"""
        alien = Alien(self)
        alien.x = alien.rect.w * (2 * col + 1)
        alien.rect.x = alien.x
        alien.y = alien.rect.h * (2 * row + 1)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _blit_bg_image(self):
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
            self.bullets.add(Bullet(self))

    def _update_screen(self):
        """Update screen state"""
        # Update background
        self._blit_bg_image()
        # Update ship state
        self.ship.blitme()
        # Draw bullets
        self.bullets.draw(self.screen)
        # Draw an alien
        self.aliens.draw(self.screen)
        # Draw an explosion
        self.explosions.draw(self.screen)
        # Display last drawn screen
        pygame.display.flip()

    def _update_bullets(self):
        """Update bullets position, remove them if they reach screen edge"""
        self.bullets.update()
        self._check_collision()

    def _check_collision(self):
        """Check bullet-alien collisions &
        update alien fleet in case of its destroying"""
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collision:
            self._create_explosion(collision)
        if not self.aliens:
            self._create_fleet()

    def _create_explosion(self, collision):
        """Add Explosion object to sprite group
        according to collision coordinates"""
        for lists in collision.values():
            for elmt in lists:
                pos_x = elmt.rect.centerx
                pos_y = elmt.rect.centery
                self.explosions.add(Explosion(self, x=pos_x, y=pos_y))

    def _check_fleet_edges(self):
        """Change fleet direction if it reaches the screen edge"""
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_dir()
                break

    def _change_fleet_dir(self):
        """Change fleet direction, (right/left)"""
        for alien in self.aliens:
            alien.rect.y += self.settings.alien_descend_speed
        self.settings.fleet_dir *= -1

    def _update_aliens(self):
        """Update positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

    def run_game(self):
        """Run main loop"""
        while True:
            self.settings.clock.tick(self.settings.fps)
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self.explosions.update()
            self._update_aliens()
            self._update_screen()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
