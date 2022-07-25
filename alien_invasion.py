import sys
import pygame

from settings import Settings

class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Run main loop"""
        while True:
            # Tracking keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen with given color
            self.screen.fill(self.settings.bg_color)

            # Display last drawn screen
            pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()