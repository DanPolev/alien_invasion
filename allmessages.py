from message import Message


def make_messages(game) -> None:
    """Create all messages according menu state"""
    music_x = game.screen_rect.centerx - 100
    music_y = game.screen_rect.centery
    music_option = Message("Music On/Off", music_x, music_y,
                           text_font=game.settings.font,
                           text_size=48)
    game.messages["options"].append(music_option)

    sound_x = game.screen_rect.centerx - 100
    sound_y = game.screen_rect.centery + 100
    sound_option = Message("Sound On/Off", sound_x, sound_y,
                           text_font=game.settings.font,
                           text_size=48)
    game.messages["options"].append(sound_option)

    centerx = game.screen_rect.centerx
    centery = game.screen_rect.centery - 100
    game_msg = Message("GAME", centerx, centery, text_font=game.settings.font,
                  text_size=100)
    game.messages["endgame"].append(game_msg)

    centery += game_msg.rect.h
    over_msg = Message("OVER!", centerx, centery, text_font=game.settings.font,
                  text_size=100)
    game.messages["endgame"].append(over_msg)

    centery += over_msg.rect.h
    press_msg = Message("Press ENTER to continue", centerx, centery,
                  text_font=game.settings.font)
    game.messages["endgame"].append(press_msg)
