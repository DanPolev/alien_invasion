import sys
import pygame

class AlienInvasion():
    """Main class for game behaviour and resources management"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 720))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Run main loop"""
        while True:
            """Tracking keyboard and mouse events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            """Display last drawn screen"""
            pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()