class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)

        # Ship settings
        self.ship_speed = 3
        self.ship_limit = 20

        #Bullet settings
        self.bullet_speed = 4.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 20

        #Alein settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Direction -1 is to the right +1 is to the left
        self.fleet_direction = 1



        