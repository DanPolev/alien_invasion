class Settings():
    """Class containing game configuration"""

    def __init__(self, screen_width = 1024, screen_height = 720):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0)
        self.ship_speed = 0.5