import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from allbutons import make_buttons
from scoreboard import Scoreboard
from message import Message, GroupMessage


class AlienInvasion:
    """Main class for game behaviour and resources management"""

    def __init__(self) -> None:
        """Initialize game and create game resources"""
        pygame.init()
        self.run = True
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion by DanPolev")

        self.stats = GameStats(self)
        self.stats.load_stats()
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bg_image = pygame.image.load("images/space_background.bmp").convert_alpha()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()

        # Menu states & flags
        self.show_menu = True
        self.menu_state = "main"

        # Create buttons
        self.buttons = {"main": [],
                        "pause": [],
                        "difficulties": [],
                        "options": [],
                        "in-game": [],
                        "endgame": []
                        }

        make_buttons(self)

        # List with all message images
        self.messages = GroupMessage()

        # Game sounds
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.button_sound = pygame.mixer.Sound("sounds/button.wav")
        self.losing_sound = pygame.mixer.Sound("sounds/losing.wav")
        self.victory_sound = pygame.mixer.Sound("sounds/victory.wav")
        pygame.mixer.music.load("sounds/bg_music.mp3")
        pygame.mixer.music.play(-1)

    def _create_fleet(self) -> None:
        """Create alien fleet"""
        alien = Alien(self)
        avail_space_x = self.screen_rect.w - 2 * alien.rect.w
        avail_space_y = self.screen_rect.h - 2 * alien.rect.h - self.ship.rect.h
        number_aliens_x = avail_space_x // (2 * alien.rect.w)
        number_aliens_y = avail_space_y // (2 * alien.rect.h)

        for row in range(number_aliens_y):
            for col in range(number_aliens_x):
                self._create_alien(row, col)

    def _create_alien(self,
                      row: int,
                      col: int) -> None:
        """Create an alien for the given row & column id"""
        alien = Alien(self)
        alien.x = alien.rect.w * (2 * col + 1)
        alien.rect.x = alien.x
        alien.y = alien.rect.h * (2 * row + 1)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _blit_bg_image(self) -> None:
        """Blit background image on the screen"""
        self.screen.blit(self.bg_image, self.screen_rect)

    def _check_events(self) -> None:
        """Process keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)
                self._execute_button()

    def _check_button(self,
                      mouse_pos: tuple[int, int]) -> None:
        """Checks if a button pressed"""
        if self.show_menu:
            for button in self.buttons[self.menu_state]:
                button.clicked = button.rect.collidepoint(mouse_pos)
                if button.clicked:
                    self.button_sound.play()

    def _execute_button(self) -> None:
        """Execute pressed button functionality"""
        for button in self.buttons[self.menu_state]:
            if button.clicked:
                button.execute()
                if button.start_game:
                    self.settings.init_dynamic_settings()
                    self._start_game()
                break

    def _check_keyup_events(self,
                            event: pygame.event.Event) -> None:
        """Process keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self,
                              event: pygame.event.Event) -> None:
        """Process keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire()
        elif event.key == pygame.K_RETURN:
            if self.menu_state == "endgame":
                self.messages.eraseall()
                self.menu_state = "main"
                self.show_menu = True
                pygame.mouse.set_visible(True)
        elif event.key == pygame.K_ESCAPE:
            if self.menu_state == "in-game" or self.menu_state == "pause":
                self.menu_state = "pause"
                self.show_menu = not self.show_menu
                self.stats.game_active = not self.stats.game_active
                pygame.mouse.set_visible(not self.stats.game_active)

    def _start_game(self) -> None:
        """Start game: reset visible objects,
            hide mouse cursor,
            set game flag in True"""
        if not self.stats.game_active:
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.stats.lvl = 1
            self.scoreboard.prep_lvl()
            self.scoreboard.prep_ships()
            self.stats.game_active = True
            # Reset screen objects: aliens, ship, bullets
            self._reset_game()
            # Hide mouse cursor
            pygame.mouse.set_visible(False)
            # Unpause music
            pygame.mixer.music.unpause()

    def _fire(self) -> None:
        """Make new bullet & add it to the bullets group"""
        if len(self.bullets) < self.settings.max_bullets:
            self.bullets.add(Bullet(self))
            self.laser_sound.play()

    def _display_buttons(self) -> None:
        """Display buttons if they are pressed"""
        if self.show_menu and not self.stats.game_active:
            for button in self.buttons[self.menu_state]:
                button.draw_button(self.screen)

    def _update_screen(self) -> None:
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
        # Display scoreboard
        self.scoreboard.show_score()
        # Display other related images
        self.messages.draw(self.screen)

        self._display_buttons()

        # Display last drawn screen
        pygame.display.flip()

    def _update_bullets(self) -> None:
        """Update bullets position, remove them if they reach screen edge"""
        self.bullets.update()
        self._check_collision()

    def _check_collision(self) -> None:
        """Check bullet-alien collisions &
        update alien fleet in case of its destroying"""
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collision:
            print(collision)
            self._create_explosion(collision)
            self._score_collision(collision)

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self) -> None:
        """Start new game level with increased difficulty.
        Recreate alien fleet"""
        # Clear current bullets & create new fleet
        self.bullets.empty()
        self.settings.increase_speed()
        self._create_fleet()
        # Increase the level
        self.stats.lvl += 1
        self.scoreboard.prep_lvl()

    def _score_collision(self,
                         collision: dict[pygame.sprite.Sprite,
                                         pygame.sprite.Sprite]) -> None:
        """Score collision for all destroyed aliens
           (even in case one bullet collision)"""
        for aliens in collision.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _create_explosion(self,
                          collision: dict[pygame.sprite.Sprite,
                                          pygame.sprite.Sprite]) -> None:
        """Add Explosion object to sprite group
        according to collision coordinates"""
        for aliens in collision.values():
            for alien in aliens:
                pos_x = alien.rect.centerx
                pos_y = alien.rect.centery
                self.explosions.add(Explosion(x=pos_x, y=pos_y,
                                              px_x=alien.rect.w,
                                              px_y=alien.rect.h))
        self.explosion_sound.play()

    def _check_fleet_edges(self) -> None:
        """Change fleet direction if it reaches the screen edge"""
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_dir()
                break

    def _change_fleet_dir(self) -> None:
        """Change fleet direction, (right/left)"""
        for alien in self.aliens:
            alien.rect.y += self.settings.alien_descend_speed
        self.settings.fleet_dir *= -1

    def _update_aliens(self) -> None:
        """Update positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check ship-alien collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if alien reach the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self) -> None:
        """Process ship hitting"""
        # Reduce player ships limit
        self.stats.ships_left -= 1
        self.scoreboard.prep_ships()

        if self.stats.ships_left > 0:
            self._reset_game()
            # Pause
            sleep(0.5)
        else:
            pygame.mixer.music.pause()
            if self.stats.high_score > self.stats.score:
                self.losing_sound.play()
            else:
                self.victory_sound.play()
            self._make_endgame_msg()
            self._end_game()

    def _make_endgame_msg(self) -> None:
        centerx = self.screen_rect.centerx
        centery = self.screen_rect.centery - 100
        msg = Message("GAME", centerx, centery, text_font=self.settings.font,
                      text_size=100)
        self.messages.add(msg)

        centery += msg.rect.h
        msg = Message("OVER!", centerx, centery, text_font=self.settings.font,
                      text_size=100)
        self.messages.add(msg)

        centery += msg.rect.h
        msg = Message("Press ENTER to continue", centerx, centery,
                      text_font=self.settings.font)
        self.messages.add(msg)

    def _end_game(self) -> None:
        for button_list in self.buttons.values():
            for button in button_list:
                button.clicked = False

        self.menu_state = "endgame"
        self.stats.game_active = False
        self.stats.write_stats()

    def _reset_game(self) -> None:
        """Reset game parameters"""
        # Remove aliens & bullets from the screen
        self.aliens.empty()
        self.bullets.empty()

        # Create new alien fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _check_aliens_bottom(self) -> None:
        """Check if aliens reach the bottom of the screen"""
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def run_game(self) -> None:
        """Run main loop"""
        while self.run:
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
