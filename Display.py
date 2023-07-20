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


def print_text(single_window, input_text, update=True, do_clear=True):
    global lock
    global main_window
    global draw_surface
    global line_spacing
    global width
    global height
    global init_done

    single_window.setText(input_text)
    print("Display:", input_text)
    return

    if init_done is False:
        print(input_text)
        return

    input_font_size = 100

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


def print_machine_and_soft(single_window, item):
    do_clear = True

    if item is not None:
        if item.get_machine_short_name() is not None:
            if print_cabinet(single_window, item) is True:
                do_clear = False

        if do_clear is True:
            if Config.title_background is not None:
                display_picture_file_name(single_window, Config.title_background)
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

        print_text_array(single_window, text_array, do_clear)


def print_text_array(single_window, text_array, do_clear):
    height_in_window = 0

    for text in text_array:
        print_text(single_window, text, True, do_clear)


def wait_for_keyboard():
    pygame.display.update()
    time.sleep(0.05)

    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

    return False


def print_cabinet(single_window, item):
    driver_name_list = [item.get_machine_short_name()]
    if item.get_cloneof_short_name() is not None:
        driver_name_list.append(item.get_cloneof_short_name())

    return display_cabinet(single_window, driver_name_list)


def display_cabinet(single_window, driver_name_list):
    if display_cabinet_picture_from_dir(single_window, driver_name_list) is True:
        return True
    return display_cabinet_picture_from_zip(single_window, driver_name_list)


def display_cabinet_picture_from_zip(single_window, driver_name_list):
    global lock
    global draw_surface

    try:
        with zipfile.ZipFile('/media/4To/Mame/cabinets.zip') as zip_file:
            for driver_name in driver_name_list:
                with zip_file.open(driver_name + '.png') as open_zip_file:
                    with open('/tmp/' + driver_name + '.png', 'wb') as dest_file:
                        print("Open cabinet picture", driver_name + '.png', "from ZIP file")
                        dest_file.write(open_zip_file.read())
                        single_window.set_pixmap('/tmp/' + driver_name + '.png')
                        return True
    except zipfile.error:
        print("ZIP file corrupted")
    except KeyError:
        pass

    return False


def display_cabinet_picture_from_dir(single_window, driver_name_list):
    try:
        for driver_name in driver_name_list:
            try:
                with open("/media/4To/Mame/cabinets/" + driver_name + '.png') as file:
                    print("Open cabinet picture from directory")
                    single_window.set_pixmap("/media/4To/Mame/cabinets/" + driver_name + '.png')
                    return True
            except FileNotFoundError:
                pass

    except zipfile.error:
        print("ZIP file corrupted")
    except KeyError:
        pass

    return False


def display_picture_file_name(single_window, file_name):
    single_window.set_pixmap(file_name)


def record_marquee():
    if Config.record is not None:
        filename = Record.get_name() + ".png"
        pygame.image.save(draw_surface, filename)


def record_title():
    if Config.record is not None:
        filename = Config.record + "/000.png"
        pygame.image.save(draw_surface, filename)
