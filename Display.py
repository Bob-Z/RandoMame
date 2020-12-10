import threading
import time

import pygame

import Desktop

main_window = None
lock = threading.Lock()
draw_surface = None


def init():
    global main_window
    global draw_surface

    pygame.display.init
    pygame.font.init()

    desktop_size = Desktop.get_desktop_size()
    main_window = pygame.display.set_mode((desktop_size[2], desktop_size[3]), flags=pygame.NOFRAME)
    draw_surface = pygame.Surface((desktop_size[2], desktop_size[3]))
    pygame.display.set_caption('RandoMame')
    print_text("RandoMame", 32, desktop_size[2] // 2, desktop_size[3] // 2)


def clear(rect):
    global lock
    global draw_surface

    lock.acquire()
    pygame.draw.rect(draw_surface, (0, 0, 0), rect)
    lock.release()


def print_text(text, font_size, x, y):
    global lock
    global main_window
    global draw_surface

    lock.acquire()

    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    draw_surface.blit(text_surface, text_rect)
    main_window.blit(draw_surface, draw_surface.get_rect())

    lock.release()


def print_window(machine_name, soft_name, font_size, position):
    rect = pygame.Rect(position['pos_x'], position['pos_y'], position['width'], position['height'])
    clear(rect)

    center_x = position['pos_x'] + position['width'] / 2
    center_y = position['pos_y'] + position['height'] / 2
    upper_half_center_y = position['pos_y'] + position['height'] / 3
    lower_half_center_y = position['pos_y'] + position['height'] * 2 / 3

    if soft_name is not None:
        print_text(soft_name, font_size, center_x, lower_half_center_y)
        print_text(machine_name, font_size, center_x, upper_half_center_y)
    else:
        print_text(machine_name, font_size, center_x, center_y)


def wait_for_keyboard():
    global lock
    while True:
        lock.acquire()
        pygame.display.update()
        lock.release()
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            break

        time.sleep(0.1)
