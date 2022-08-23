import pygame.font


class Scoreboard():
    """Game info output class"""
    def __init__(self, game):
        """Initialize attributes for game scoring"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for score output
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare initial image
        self.prep_score()

    def prep_score(self):
        """Convert current score to the image"""
        score_str = f"Kills: {self.stats.score}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color)

        # Output scoreboard at top-right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Print scoreboard onto the screen"""
        self.screen.blit(self.score_image, self.score_rect)


