class Settings():
    """Class containing game configuration"""

    def __init__(self):
        """Initialize game settings"""
        # Ship settings
        self.ship_speed = 2

        # Bullet settings
        self.bullet_speed = 4
        self.bullet_width = 6
        self.bullet_height = 12
        self.bullet_color = (255,0,0)
        self.max_bullets = 3

