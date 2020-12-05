import pygame

import Desktop


def init():
    pygame.display.init
    pygame.font.init()

    desktop_size = Desktop.get_desktop_size()
    main_window = pygame.display.set_mode((desktop_size[2], desktop_size[3]), flags=pygame.NOFRAME)
    pygame.display.set_caption('RandoMame')
    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 32)
    text = font.render('RandoMame', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (desktop_size[2] // 2, desktop_size[3] // 2)
    main_window.blit(text, textRect)
    pygame.display.update()


def wait_for_keyboard():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            exit(0)
