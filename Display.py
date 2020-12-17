import os
import threading

import pygame

import Desktop

main_window = None
lock = threading.Lock()
draw_surface = None
line_spacing = -2
border_margin = 0.95
window_x = None
window_y = None
width = None
height = None


def init(desktop):
    global main_window
    global draw_surface
    global window_x
    global window_y
    global width
    global height

    window_x = desktop[0]
    window_y = desktop[1]
    width = desktop[2]
    height = desktop[3]

    pygame.display.init
    pygame.font.init()

    main_window = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)
    pygame.display.set_caption('RandoMame')

    desktop = Desktop.DesktopClass()
    desktop.set_position(os.getpid(), window_x, window_y, width, height)

    draw_surface = pygame.Surface((width, height))
    print_text("RandoMame", None)


def clear(rect):
    global lock
    global draw_surface

    lock.acquire()
    pygame.draw.rect(draw_surface, (0, 0, 0), rect)
    lock.release()


def print_compute_parameters(input_text, input_font_size, dest_rect, first=True):
    global line_spacing
    global border_margin

    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', input_font_size)

    # get the height of the font
    font_height = font.size("Tg")[1]

    y = 0
    text = input_text
    max_width = 0

    wrapped = False
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > dest_rect.bottom:
            y -= line_spacing
            wrapped = True
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < (dest_rect.width * border_margin) and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            wrapped = True
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

    if wrapped is True and first is False:
        return None, None, None, None

    next_offset_x, next_offset_y, next_max_width, next_font_size = print_compute_parameters(input_text,
                                                                                            input_font_size + 2,
                                                                                            dest_rect, False)

    if next_offset_x is None:
        return offset_x, offset_y, max_width, input_font_size

    return next_offset_x, next_offset_y, next_max_width, next_font_size


def print_text(input_text, dest_rect, update=True):
    global lock
    global main_window
    global draw_surface
    global line_spacing
    global width
    global height

    input_font_size = 32

    if dest_rect is None:
        dest_rect = pygame.Rect(0, 0, width, height)

    clear(dest_rect)

    offset_x, offset_y, max_width, font_size = print_compute_parameters(input_text, input_font_size, dest_rect)

    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)

    # get the height of the font
    font_height = font.size("Tg")[1]

    y = dest_rect.top
    text = input_text

    lock.acquire()

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

        line_offset_x = (max_width - font.size(text[:i])[0]) / 2
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x, y + offset_y))
        y += font_height + line_spacing

        # remove the text we have just blitted
        text = text[i:]

    main_window.blit(draw_surface, draw_surface.get_rect())

    if update is True:
        pygame.display.update()

    lock.release()


def print_window(machine_name, soft_name, position):
    rect = pygame.Rect(position['pos_x'], position['pos_y'], position['width'], position['height'])

    if soft_name is not None:
        upper_rect = pygame.Rect(rect.left, rect.top, rect.width, rect.height / 2)
        print_text(soft_name, upper_rect, False)
        lower_rect = pygame.Rect(rect.left, rect.top + rect.height / 2, rect.width, rect.height / 2)
        print_text(machine_name, lower_rect, False)
    else:
        print_text(machine_name, rect, False)


def wait_for_keyboard():
    pygame.display.update()

    event = pygame.event.wait(100)
    if event.type == pygame.KEYDOWN:
        return True
    else:
        return False
