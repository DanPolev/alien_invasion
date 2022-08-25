import pygame.font


class Button():
    """Button class"""
    def __init__(self, image, centerx=0, centery=0, scale=1, msg=""):
        """Button attributes initialization"""
        # Button figure
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,
                                            (width * scale, height * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)

        # Is button clicked
        self.clicked = False

        # Text properties
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Prepare message to be displayed"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, surface):
        """Display an empty button & message afterwards"""
        surface.blit(self.image, self.rect)
        surface.blit(self.msg_image, self.msg_image_rect)

    #def move_button(self, centerx, centery):
    #    self.rect.centerx = centerx
    #    self.rect.centery = centery
    #    self.msg_image_rect.center = self.rect.center