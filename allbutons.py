import pygame
import button as mybutton


def make_buttons(game) -> None:
    """Make all buttons"""
    button_image = pygame.image.load("images/button.bmp").convert_alpha()

    x_play = game.screen_rect.centerx
    y_play = game.screen_rect.centery - 50
    play_button = mybutton.PlayButton(game, button_image, centerx=x_play,
                                      centery=y_play, scale=0.1)
    game.buttons["main"].append(play_button)

    y_option = y_play + play_button.rect.h
    option_button = mybutton.OptionsButton(game, button_image,
                                           centerx=x_play, centery=y_option,
                                           scale=0.1)
    game.buttons["main"].append(option_button)

    y_quit_main = y_option + play_button.rect.h
    quit_main_button = mybutton.QuitButton(game, button_image,
                                           centerx=x_play,
                                           centery=y_quit_main, scale=0.1)
    game.buttons["main"].append(quit_main_button)

    y_resume = game.screen_rect.centery - play_button.rect.h
    resume_button = mybutton.ResumeButton(game, button_image,
                                          centerx=x_play, centery=y_resume,
                                          scale=0.1)
    game.buttons["pause"].append(resume_button)

    y_restart = y_resume + resume_button.rect.h
    restart_button = mybutton.RestartButton(game, button_image,
                                            centerx=x_play,
                                            centery=y_restart, scale=0.1)
    game.buttons["pause"].append(restart_button)

    #y_option = y_restart + restart_button.rect.h
    #option_button = mybutton.OptionsButton(game, button_image,
    #                                       centerx=x_play, centery=y_option,
    #                                       scale=0.1)
    #game.buttons["pause"].append(option_button)

    y_quit_pause = y_restart + option_button.rect.h
    quit_pause_button = mybutton.QuitButton(game, button_image,
                                            centerx=x_play,
                                            centery=y_quit_pause, scale=0.1)
    game.buttons["pause"].append(quit_pause_button)

    easy_button = mybutton.DifficultyButton(game, button_image, "Easy",
                                            centerx=x_play, centery=y_play,
                                            scale=0.1)
    game.buttons["difficulties"].append(easy_button)

    y_medium = y_play + easy_button.rect.h
    medium_button = mybutton.DifficultyButton(game, button_image, "Medium",
                                              centerx=x_play,
                                              centery=y_medium, scale=0.1)
    game.buttons["difficulties"].append(medium_button)

    y_hard = y_medium + medium_button.rect.h
    hard_button = mybutton.DifficultyButton(game, button_image, "Hard",
                                            centerx=x_play, centery=y_hard,
                                            scale=0.1)
    game.buttons["difficulties"].append(hard_button)

    x_back = game.screen_rect.right - 100
    y_back = game.screen_rect.bottom - 50
    back_button = mybutton.BackButton(game, button_image,
                                      prev_menu_state="main",
                                      centerx=x_back, centery=y_back,
                                      scale=0.08)
    game.buttons["options"].append(back_button)
    game.buttons["difficulties"].append(back_button)

    x_tickbox = game.screen_rect.centerx + 150
    y_tickbox = game.screen_rect.centery
    tickbox = mybutton.TickBox(game, game.music_player,
                               x_tickbox, y_tickbox)
    game.buttons["options"].append(tickbox)

    x_tickbox = game.screen_rect.centerx + 150
    y_tickbox = game.screen_rect.centery + 100
    tickbox = mybutton.TickBox(game, game.sound_player,
                               x_tickbox, y_tickbox)
    game.buttons["options"].append(tickbox)
