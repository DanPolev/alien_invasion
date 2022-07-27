class Settings():
    """Class containing game configuration"""

    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 1024
        self.screen_height = 720

        # Ship settings
        self.ship_speed = 2

        # Bullet settings
        self.bullet_speed = 4
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255,0,0)
        self.max_bullets = 3

