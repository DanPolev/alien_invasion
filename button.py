import pygame

from toggle import Toggle


class Button:
    """Button class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 msg: str = "",
                 font_size: int = 46) -> None:
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
        self.font = pygame.font.SysFont(self.settings.font, font_size)

        self._prep_msg(msg)

        # Flag for Restart and difficulties buttons to start/restart game
        self.start_game = False

    def _prep_msg(self, msg: str) -> None:
        """Prepare message to be displayed"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self, surface: pygame.Surface) -> None:
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
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Play",
                        font_size)

    def execute(self) -> None:
        """Execute button function: switch menu_state to difficulty choice"""
        self.game.menu_state = "difficulties"


class ResumeButton(Button):
    """ResumeButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Resume",
                        font_size)

    def execute(self) -> None:
        """Execute button function: hide menu & cursor, resume game"""
        self.game.menu_state = "in-game"
        self.game.show_menu = False
        self.game.stats.game_active = True
        pygame.mouse.set_visible(False)


class QuitButton(Button):
    """QuitButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Quit",
                        font_size)

    def execute(self) -> None:
        """Execute button function: end game"""
        self.game.run = False


class RestartButton(Button):
    """RestartButton class"""
    def __init__(self, game,
                 image: pygame.Surface,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Restart",
                        font_size)

    def execute(self) -> None:
        """Execute button function: restart game process"""
        self.game.menu_state = "in-game"
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
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, msg,
                        font_size)
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
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Option",
                        font_size)

    def execute(self) -> None:
        """Switch menu_state to options choice"""
        self.game.menu_state = "options"
        

class BackButton(Button):
    def __init__(self, game,
                 image: pygame.Surface,
                 prev_menu_state: str,
                 centerx: int = 0,
                 centery: int = 0,
                 scale: float = 1,
                 font_size: int = 46) -> None:
        Button.__init__(self, game, image, centerx, centery, scale, "Back",
                        font_size)
        self.prev_menu_state = prev_menu_state

    def execute(self) -> None:
        self.game.menu_state = self.prev_menu_state


class TickBox(Button):
    def __init__(self, game,
                 switch_param: Toggle,
                 centerx: int = 0,
                 centery: int = 0) -> None:
        """Initialize TickBox: make tickbox image, take switch parameter"""
        self.width = 50
        self.height = 50
        self.switch_param = switch_param
        self._make_emptybox_img()
        self.make_tickedbox_img()

        Button.__init__(self, game, self.tickedbox_img, centerx, centery)

    def _make_emptybox_img(self):
        """Make empty tickbox image"""
        self.emptybox_img = pygame.Surface((self.width, self.height))
        rect = self.emptybox_img.get_rect()
        white = (255, 255, 255)
        red = (255, 0, 0)
        self.emptybox_img.fill(white, rect)
        pygame.draw.rect(self.emptybox_img, red, rect, width=5)

    def make_tickedbox_img(self):
        self.tickedbox_img = pygame.image.load("images/x_mark.bmp")
        self.tickedbox_img = pygame.transform.scale(self.tickedbox_img,
                                                    (self.width, self.height))
        rect = self.tickedbox_img.get_rect()
        red = (255, 0, 0)
        pygame.draw.rect(self.tickedbox_img, red, rect, width=5)

    def execute(self) -> None:
        """Switch given switch_parameter and draw/hide a tick mark"""
        self.switch_param.toggle()
        if self.switch_param.status:
            self.image = self.tickedbox_img
        else:
            self.image = self.emptybox_img
