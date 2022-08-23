import os

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

    def load_stats(self):
        """Load best result data"""
        if not os.path.isdir("local"):
            os.mkdir("local")
        else:
            try:
                with open("local/best_result.txt", encoding="utf-8") as f:
                    self.high_score = int(f.read())
            except FileNotFoundError:
                pass

    def write_stats(self):
        """Write best result to the file"""
        with open("local/best_result.txt", "w") as f:
            f.write(str(round(self.high_score, -1)))
