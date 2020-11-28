import pygame


def init():
    pygame.init()
    main_window = pygame.display.set_mode((Config.desktop[2], Config.desktop[3]), flags=pygame.NOFRAME)
    pygame.display.set_caption('RandoMame')
    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 32)
    text = font.render('RandoMame', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (Config.desktop[2] // 2, Config.desktop[3] // 2)
    main_window.blit(text, textRect)
    pygame.display.update()
