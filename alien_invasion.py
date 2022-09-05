import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from button import Button
from scoreboard import Scoreboard


class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
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

        self.show_menu = True
        self.menu_state = "start"

        # Create buttons
        self.buttons = {}
        self.menu_states = {"main" : ["Resume", "Restart", "Quit"],
                            "start" : ["Play", "Quit"],
                            "difficulties" : ["Easy", "Medium", "Hard"],
                             }
        self._make_buttons()

    def _make_buttons(self):
        """Make all buttons"""
        button_image = pygame.image.load("images/button.bmp").convert_alpha()

        x_play = self.screen_rect.centerx
        y_play = self.screen_rect.centery
        play_button = Button(button_image, centerx=x_play, centery=y_play,
                             scale=0.1, msg="Play")
        self.buttons["Play"] = play_button

        y_quit = y_play + 2 * play_button.rect.h
        quit_button = Button(button_image, centerx=x_play, centery=y_quit,
                             scale=0.1, msg="Quit")
        self.buttons["Quit"] = quit_button

        resume_button = Button(button_image, centerx=x_play, centery=y_play,
                               scale=0.1, msg="Resume")
        self.buttons["Resume"] = resume_button

        y_restart = y_play + resume_button.rect.h
        restart_button = Button(button_image, centerx=x_play,centery=y_restart,
                                scale=0.1, msg="Restart")
        self.buttons["Restart"] = restart_button

        easy_button = Button(button_image, centerx=x_play, centery=y_play,
                             scale=0.1, msg="Easy")
        self.buttons["Easy"] = easy_button

        y_medium = y_play + easy_button.rect.h
        medium_button = Button(button_image, centerx=x_play, centery=y_medium,
                               scale=0.1, msg="Medium")
        self.buttons["Medium"] = medium_button

        y_hard = y_medium + medium_button.rect.h
        hard_button = Button(button_image, centerx=x_play, centery=y_hard,
                             scale=0.1, msg="Hard")
        self.buttons["Hard"] = hard_button

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
                self.run = False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)
                self._execute_button()

    def _check_button(self, mouse_pos):
        """Checks if a button pressed"""
        if self.menu_state == "start" and self.show_menu:
            self.buttons["Play"].clicked = self.buttons[
                "Play"].rect.collidepoint(mouse_pos)
            self.buttons["Quit"].clicked = self.buttons[
                "Quit"].rect.collidepoint(mouse_pos)
        elif self.menu_state == "main" and self.show_menu:
            self.buttons["Resume"].clicked = self.buttons[
                "Resume"].rect.collidepoint(mouse_pos)
            self.buttons["Restart"].clicked = self.buttons[
                "Restart"].rect.collidepoint(mouse_pos)
            self.buttons["Quit"].clicked = self.buttons[
                "Quit"].rect.collidepoint(mouse_pos)
        elif self.menu_state == "difficulties" and self.show_menu:
            self.buttons["Easy"].clicked = self.buttons[
                "Easy"].rect.collidepoint(mouse_pos)
            self.buttons["Medium"].clicked = self.buttons[
                "Medium"].rect.collidepoint(mouse_pos)
            self.buttons["Hard"].clicked = self.buttons[
                "Hard"].rect.collidepoint(mouse_pos)

    def _execute_button(self):
        """Execute pressed button functionality"""
        if self.menu_state == "start":
            if self.buttons["Play"].clicked:
                self.menu_state = "difficulties"
            elif self.buttons["Quit"].clicked:
                self.run = False
        elif self.menu_state == "main":
            if self.buttons["Resume"].clicked:
                self.show_menu = False
                self.stats.game_active = True
                pygame.mouse.set_visible(False)
            elif self.buttons["Restart"].clicked:
                self.show_menu = False
                self.stats.game_active = False
                self.settings.init_dynamic_settings()
                self._start_game()
            elif self.buttons["Quit"].clicked:
                self.run = False
        elif self.menu_state == "difficulties":
            self.show_menu = False
            avail_buttons = self.menu_states[self.menu_state]
            for key, button in self.buttons.items():
                if key in avail_buttons and button.clicked:
                    self.settings.speedup_scale = self.settings.difficulties[key]
                    self.settings.score_scale = self.settings.score_scales[key]
                    break
            self.menu_state = "in-game"
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
        elif (event.key == pygame.K_SPACE and
            self.stats.game_active):
            self._fire()
        elif event.key == pygame.K_p:
            self.buttons["Play"].clicked = True
        elif event.key == pygame.K_ESCAPE:
            if (self.buttons["Play"].clicked and
                    self.menu_state != "difficulties"):
                self.menu_state = "main"
                self.show_menu = not self.show_menu
                self.stats.game_active = not self.stats.game_active
                pygame.mouse.set_visible(not self.stats.game_active)

    def _start_game(self):
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

    def _fire(self):
        """Make new bullet & add it to the bullets group"""
        if len(self.bullets) < self.settings.max_bullets:
            self.bullets.add(Bullet(self))

    def _display_buttons(self):
        """Display buttons if they are pressed"""
        if self.show_menu and not self.stats.game_active:
            avail_buttons = self.menu_states[self.menu_state]
            for key, button in self.buttons.items():
                if key in avail_buttons:
                    button.draw_button(self.screen)

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
        # Display scoreboard
        self.scoreboard.show_score()

        self._display_buttons()

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
            self._score_collision(collision)

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Start new game level with increased difficulty.
        Recreate alien fleet"""
        # Clear current bullets & create new fleet
        self.bullets.empty()
        self.settings.increase_speed()
        self._create_fleet()
        # Increase the level
        self.stats.lvl += 1
        self.scoreboard.prep_lvl()

    def _score_collision(self, collision):
        """Score collision for all destroyed aliens
           (even in case one bullet collision)"""
        for aliens in collision.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _create_explosion(self, collision):
        """Add Explosion object to sprite group
        according to collision coordinates"""
        for lists in collision.values():
            for elmt in lists:
                pos_x = elmt.rect.centerx
                pos_y = elmt.rect.centery
                self.explosions.add(Explosion(x=pos_x, y=pos_y,
                                              px_x=elmt.rect.w,
                                              px_y=elmt.rect.h))

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
        self.stats.ships_left -= 1
        self.scoreboard.prep_ships()

        if self.stats.ships_left > 0:
            self._reset_game()
            # Pause
            sleep(0.5)  # TODO: add player ship destroying animation
        else:
            self._end_game()

    def _end_game(self):
        for button in self.buttons.values():
            button.clicked = False

        self.menu_state = "start"
        self.show_menu = True
        self.stats.game_active = False
        self.stats.write_stats()
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
