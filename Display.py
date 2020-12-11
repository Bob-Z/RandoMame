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
    print_text("RandoMame", 32, pygame.Rect(0,0,desktop_size[2], desktop_size[3]))


def clear(rect):
    global lock
    global draw_surface

    lock.acquire()
    pygame.draw.rect(draw_surface, (0, 0, 0), rect)
    lock.release()


def print_text_(text, font_size, x, y):
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


def print_text(input_text, font_size, dest_rect):
    global lock
    global main_window
    global draw_surface

    lock.acquire()

    line_spacing = -2

    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)

    # get the height of the font
    font_height = font.size("Tg")[1]

    y = 0
    text = input_text
    max_width = 0
    
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > dest_rect.bottom:
            y -= line_spacing
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < dest_rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            j = text.rfind(" ", 0, i) + 1
            if j > 0:
                i = j
            else:
                i -= 1

        max_width = max(max_width, font.size(text[:i])[0])
        y += font_height + line_spacing

        # remove the text we have just blitted
        text = text[i:]

    offset_x = (dest_rect.width - max_width) / 2
    offset_y = (dest_rect.height - y) / 2

    y = dest_rect.top
    text = input_text
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > dest_rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < dest_rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            j = text.rfind(" ", 0, i) + 1
            if j > 0:
                i = j
            else:
                i -= 1

        image = font.render(text[:i], True, (255, 255, 255))

        draw_surface.blit(image, (dest_rect.left + offset_x, y + offset_y))
        y += font_height + line_spacing

        # remove the text we have just blitted
        text = text[i:]

    main_window.blit(draw_surface, draw_surface.get_rect())
    pygame.display.update()

    lock.release()


def print_window(machine_name, soft_name, font_size, position):
    rect = pygame.Rect(position['pos_x'], position['pos_y'], position['width'], position['height'])
    clear(rect)

    if soft_name is not None:
        upper_rect = pygame.Rect(rect.left, rect.top, rect.width, rect.height/2)
        print_text(soft_name, font_size, upper_rect)
        lower_rect = pygame.Rect(rect.left, rect.top + rect.height/2, rect.width, rect.height / 2)
        print_text(machine_name, font_size, lower_rect)
    else:
        print_text(machine_name, font_size, rect)


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
