import pygame


class Button():
    """Button class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 msg: str = "") -> None:
        """Button attributes initialization"""
        self.game = game
        self.settings = self.game.settings

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
        self.font = pygame.font.SysFont(self.settings.font, 46)

        self._prep_msg(msg)

        # Flag for Restart and difficulties buttons to start/restart game
        self.start_game = False

    def _prep_msg(self, msg: str) -> None:
        """Prepare message to be displayed"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, surface: pygame.Surface) -> None:
        """Display an empty button & message afterwards"""
        surface.blit(self.image, self.rect)
        surface.blit(self.msg_image, self.msg_image_rect)

    def execute(self) -> None:
        """Execute button function"""
        pass


class PlayButton(Button):
    """PlayButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Play")

    def execute(self) -> None:
        """Execute button function: switch menu_state to difficulty choice"""
        self.game.menu_state = "difficulties"


class ResumeButton(Button):
    """ResumeButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Resume")

    def execute(self) -> None:
        """Execute button function: hide menu & cursor, resume game"""
        self.game.show_menu = False
        self.game.stats.game_active = True
        pygame.mouse.set_visible(False)


class QuitButton(Button):
    """QuitButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Quit")

    def execute(self) -> None:
        """Execute button function: end game"""
        self.game.run = False


class RestartButton(Button):
    """RestartButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Restart")

    def execute(self) -> None:
        """Execute button function: restart game process"""
        self.game.show_menu = False
        self.game.stats.game_active = False
        self.start_game = True


class DifficultyButton(Button):
    """DifficultyButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 msg: str,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, msg)
        self.msg = msg

    def execute(self) -> None:
        """Execute button function: set difficulty &
        speedup/score scales params"""
        self.game.show_menu = False
        self.game.menu_state = "in-game"
        self.start_game = True
        self.settings.speedup_scale = self.settings.difficulties[self.msg]
        self.settings.score_scale = self.settings.score_scales[self.msg]


class OptionsButton(Button):
    """OptionsButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Option")

    def execute(self) -> None:
        """Switch menu_state to options choice"""
        self.game.menu_state = "options"
