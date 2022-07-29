class Settings():
    """Class containing game configuration"""

    def __init__(self):
        """Initialize game settings"""
        # Ship settings
        self.ship_speed = 3

        # Bullet settings
        self.bullet_speed = 4
        self.max_bullets = 3

        # Alien settings
        self.alien_speed = 1
        self.alien_descend_speed = 10
        # fleet_dir = 1 -> moving right; = -1 -> moving left
        self.fleet_dir = 1
