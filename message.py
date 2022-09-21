import pygame


class Message():
    """Contains image and image rectangle for message creation"""
    def __init__(self, msg="", centerx=0, centery=0, text_color=(255, 255, 255),
                 text_size=48, text_font=None):
        """Create new image for the message"""
        font = pygame.font.SysFont(text_font, text_size)
        self.image = font.render(msg, True, text_color)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)

    def draw(self, surface):
        """Draw a message on the surface"""
        surface.blit(self.image, self.rect)


class GroupMessage():
    def __init__(self):
        self.messages = []

    def add(self, msg):
        self.messages.append(msg)

    def draw(self, surface):
        for message in self.messages:
            message.draw(surface)

    def eraseall(self):
        self.messages.clear()