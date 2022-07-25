import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def _check_events(self):
        """Process keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Update screen state"""
        # Redraw the screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Display last drawn screen
        pygame.display.flip()

    def run_game(self):
        """Run main loop"""
        while True:
            self._check_events()
            self._update_screen()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()