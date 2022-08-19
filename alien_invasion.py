import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from button import Button


class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion by DanPolev")
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bg_image = pygame.image.load("images/space_background.bmp").convert_alpha()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()

        # Create Play button
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        """Create alien fleet"""
        alien = Alien(self)
        avail_space_x = self.screen_rect.w - 2 * alien.rect.w
        avail_space_y = self.screen_rect.h - 2 * alien.rect.h - self.ship.rect.h
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Checks if play button pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset dynamic game settings before game start
            self.settings.init_dynamic_settings()
            self._start_game()

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
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _start_game(self):
        """Start game: reset visible objects,
            hide mouse cursor,
            set game flag in True"""
        if not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            # Reset screen objects: aliens, ship, bullets
            self._reset_game()
            # Hide mouse cursor
            pygame.mouse.set_visible(False)

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

        # Display Play button if the game is not active
        if not self.stats.game_active:
            self.play_button.draw_button()

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
            self.bullets.empty()
            self.settings.increase_speed()
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

        # Check ship-alien collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if alien reach the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Process ship hitting"""
        # Reduce player ships limit
        self.settings.ship_limit -= 1

        if self.settings.ship_limit > 0:
            self._reset_game()
            # Pause
            sleep(0.5)  # TODO: add player ship destroying animation
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _reset_game(self):
        """Reset game parameters"""
        # Remove aliens & bullets from the screen
        self.aliens.empty()
        self.bullets.empty()

        # Create new alien fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _check_aliens_bottom(self):
        """Check if aliens reach the bottom of the screen"""
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def run_game(self):
        """Run main loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self.explosions.update()
                self._update_aliens()

            self._update_screen()
            self.settings.clock.tick(self.settings.fps)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
