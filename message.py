import pygame


class Message():
    """Contains image and image rectangle for message creation"""
    def __init__(self, msg: str = "",
                 centerx: int = 0,centery: int = 0,
                 text_color: tuple[int, int, int]=(255, 255, 255),
                 text_size: int = 48,
                 text_font: str = None) -> None:
        """Create new image for the message"""
        font = pygame.font.SysFont(text_font, text_size)
        self.image = font.render(msg, True, text_color)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw a message on the surface"""
        surface.blit(self.image, self.rect)


class GroupMessage():
    def __init__(self) -> None:
        self.messages = []

    def add(self, msg: str) -> None:
        """Add Message to the Group list"""
        self.messages.append(msg)

    def draw(self, surface: pygame.Surface) -> None:
        """Blit message image on the pygame.Surface"""
        for message in self.messages:
            message.draw(surface)

    def eraseall(self) -> None:
        self.messages.clear()