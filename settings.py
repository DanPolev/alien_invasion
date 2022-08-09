import pygame


class Settings():
    """Class containing game configuration"""

    def __init__(self):
        """Initialize game settings"""
        # Time settings
        self.clock = pygame.time.Clock()
        self.fps = 140

        # Ship settings
        self.ship_speed = 3
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 4
        self.max_bullets = 3

        # Alien settings
        self.alien_speed = 5
        self.alien_descend_speed = 15
        # fleet_dir = 1 -> moving right; = -1 -> moving left
        self.fleet_dir = 1
