class GameStats():
    """Statistics tracking for the game"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Initialize the statistics changing during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.lvl = 1
