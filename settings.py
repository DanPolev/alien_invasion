import pygame


class Settings():
    """Class containing game configuration"""

    def __init__(self):
        """Initialize static game settings"""
        # Time settings
        self.clock = pygame.time.Clock()
        self.fps = 140

        # Difficulty settings
        self.difficulties = {"Easy" : 1.1, "Medium" : 1.25, "Hard" : 1.5}

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.max_bullets = 3

        # Alien settings
        self.alien_descend_speed = 10

        # Game speedup ratio
        self.speedup_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed = 3
        self.alien_speed = 3
        self.bullet_speed = 4

        # fleet_dir = 1 -> moving right; = -1 -> moving left
        self.fleet_dir = 1

        # Set difficulty level up
        self.increase_speed()

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

