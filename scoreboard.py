import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """Game info output class"""
    def __init__(self, game):
        """Initialize attributes for game scoring"""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for score output
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare initial images
        self.prep_score()
        self.prep_high_score()
        self.prep_lvl()
        self.prep_ships()

    def prep_score(self):
        """Convert current score to the image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Scores: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color)

        # Output scoreboard at top-right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Convert high score to the image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "Best: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color)

        # High score is located at the top-center point of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_lvl(self):
        """Convert level to image"""
        lvl_str = f"Level: {self.stats.lvl}"
        self.lvl_image = self.font.render(lvl_str, True, self.text_color)
        self.lvl_rect = self.lvl_image.get_rect()
        # Located at the top-right corner -- under the scores
        self.lvl_rect.right = self.score_rect.right
        self.lvl_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Draw number of remaining player ship images"""
        self.ships = Group()
        for ship_id in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.image = pygame.transform.scale(ship.image,
                                            (ship.rect.w / 2, ship.rect.h / 2))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_id * ship.rect.w
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scoreboard onto the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.lvl_image, self.lvl_rect)
        self.ships.draw(self.screen)
