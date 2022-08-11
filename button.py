import pygame.font

class Button():
    """Button class"""
    def __init__(self, ai_game, msg):
        """Button attributes initialization"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Button figure
        self.image = pygame.image.load("images/button.bmp")
        self.image = pygame.transform.scale(self.image, (200, 80))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        # Text properties
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Prepare message to be displayed"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Display an empty button & message afterwards"""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)