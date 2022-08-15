import os
import threading
import time
import zipfile

import pygame

import Desktop
import Record
import Config

init_done = False
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
    global init_done

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
    print_text("RandoMame")

    init_done = True


def clear(rect):
    global draw_surface

    pygame.draw.rect(draw_surface, (0, 0, 0), rect)


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
        if y + font_height > dest_rect.height:
            y -= line_spacing
            wrapped = True
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < (dest_rect.width * border_margin) and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            wrapped = True

            # Keep parenthesis on 1 line
            a = text.rfind("(", 0, i)
            b = text.rfind(")", 0, i)

            if b >= a:
                j = text.rfind(" ", 0, i) + 1
            else:
                j = a

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


def print_text(input_text, dest_rect=None, update=True, do_clear=True):
    global lock
    global main_window
    global draw_surface
    global line_spacing
    global width
    global height
    global init_done

    if init_done is False:
        print(input_text)
        return

    input_font_size = 100

    if dest_rect is None:
        dest_rect = pygame.Rect(0, 0, width, height)

    offset_x, offset_y, max_width, font_size = print_compute_parameters(input_text, input_font_size, dest_rect)

    font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)

    # get the height of the font
    font_height = font.size("Tg")[1]

    y = 0
    text = input_text

    lock.acquire()

    if do_clear is True:
        clear(dest_rect)

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > dest_rect.height:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < dest_rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):

            # Keep parenthesis on 1 line
            a = text.rfind("(", 0, i)
            b = text.rfind(")", 0, i)

            if b >= a:
                j = text.rfind(" ", 0, i) + 1
            else:
                j = a

            if j > 0:
                i = j
            else:
                i -= 1

        line_offset_x = (max_width - font.size(text[:i])[0]) / 2

        image = font.render(text[:i], True, (0, 0, 0))
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x + 1, dest_rect.top + y + offset_y + 1))
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x + 1, dest_rect.top + y + offset_y - 1))
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x - 1, dest_rect.top + y + offset_y + 1))
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x - 1, dest_rect.top + y + offset_y - 1))

        image = font.render(text[:i], True, (255, 255, 255))
        draw_surface.blit(image, (dest_rect.left + offset_x + line_offset_x, dest_rect.top + y + offset_y))
        y += font_height + line_spacing

        # remove the text we have just blitted
        text = text[i:]

    main_window.blit(draw_surface, draw_surface.get_rect())

    if update is True:
        try:
            pygame.display.update()
        except pygame.error:
            pass

    lock.release()

    print("Display:", input_text)


def print_machine_and_soft(item, position):
    do_clear = True

    if item is not None:
        rect = pygame.Rect(position['pos_x'], position['pos_y'], position['width'], position['height'])

        if item.get_machine_short_name() is not None:
            if print_cabinet(item, rect) is True:
                do_clear = False

        if do_clear is True:
            if Config.title_background is not None:
                display_picture_file_name(Config.title_background, rect)
                do_clear = False

        text_array = []
        if item.get_soft_xml() is not None and item.get_machine_xml() is not None:
            soft_name = item.get_soft_full_description() + "[" + item.get_soft_short_name() + "]"
            text_array.append(soft_name)
            Record.log(soft_name)
            text_array.append(item.get_machine_full_description() + "[" + item.get_machine_short_name() + "]")
        else:
            if item.get_machine_xml() is not None:
                machine_name = item.get_machine_full_description() + "[" + item.get_machine_short_name() + "]"
                text_array.append(machine_name)
                Record.log(machine_name)
            else:  # vgmplay
                text_array.append(item.get_soft_full_description())
                text_array.append(item.get_part_name())
                Record.log(item.get_part_name())

        print_text_array(position, text_array, do_clear)


def print_text_array(position, text_array, do_clear):
    if position is None:
        screen_rect = pygame.Rect(0, 0, width, height)
    else:
        screen_rect = pygame.Rect(position['pos_x'], position['pos_y'], position['width'], position['height'])

    height_in_window = 0

    for text in text_array:
        rect = pygame.Rect(screen_rect.left, screen_rect.top + height_in_window, screen_rect.width,
                           screen_rect.height / len(text_array))
        print_text(text, rect, True, do_clear)
        height_in_window = height_in_window + (screen_rect.height / len(text_array))


def wait_for_keyboard():
    pygame.display.update()
    time.sleep(0.05)

    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

    return False


def print_cabinet(item, rect):
    clear(rect)

    driver_name_list = [item.get_machine_short_name()]
    if item.get_cloneof_short_name() is not None:
        driver_name_list.append(item.get_cloneof_short_name())

    return display_cabinet(driver_name_list, rect)


def display_cabinet(driver_name_list, rect):
    if display_cabinet_picture_from_dir(driver_name_list, rect) is True:
        return True
    return display_cabinet_picture_from_zip(driver_name_list, rect)


def display_cabinet_picture_from_zip(driver_name_list, rect):
    global lock
    global draw_surface

    try:
        with zipfile.ZipFile('/media/4To/Mame/cabinets.zip') as zip_file:
            for driver_name in driver_name_list:
                try:
                    with zip_file.open(driver_name + '.png') as file:
                        print("Open cabinet picture from ZIP file")
                        display_picture_file(file, rect, 128)
                        return True
                except zipfile.error:
                    print("ZIP file corrupted")
                except KeyError:
                    pass

    except zipfile.error:
        print("ZIP file corrupted")
    except KeyError:
        pass

    return False


def display_cabinet_picture_from_dir(driver_name_list, rect):
    try:
        for driver_name in driver_name_list:
            try:
                with open("/media/4To/Mame/cabinets/" + driver_name + '.png') as file:
                    print("Open cabinet picture from directory")
                    display_picture_file(file, rect, 128)
                    return True
            except FileNotFoundError:
                pass

    except zipfile.error:
        print("ZIP file corrupted")
    except KeyError:
        pass

    return False


def display_picture_file_name(file_name, rect):
    with open(file_name) as file:
        display_picture_file(file, rect, 255)


def display_picture_file(file, rect, alpha):
    global lock
    global draw_surface

    if rect is None:
        rect = pygame.Rect(0, 0, width, height)

    print("Display picture", file.name, "in", rect)

    picture = pygame.image.load(file)

    pict_rect = picture.get_rect()

    factor = rect.width / pict_rect.width
    new_width = rect.width
    new_height = int(pict_rect.height * factor)
    if new_height > rect.height:
        factor = rect.height / pict_rect.height
        new_width = int(pict_rect.width * factor)
        new_height = rect.height

    picture = pygame.transform.scale(picture, (new_width, new_height))

    pict_rect = picture.get_rect()
    pict_rect.center = rect.center

    lock.acquire()
    # black screen
    pygame.draw.rect(draw_surface, (0,0,0), rect)
    picture.set_alpha(alpha)

    draw_surface.blit(picture, pict_rect)
    lock.release()


def record_marquee():
    if Config.record is not None:
        filename = Record.get_name() + ".png"
        pygame.image.save(draw_surface, filename)


def record_title():
    if Config.record is not None:
        filename = Config.record + "/000.png"
        pygame.image.save(draw_surface, filename)
