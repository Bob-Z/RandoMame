#!/usr/bin/python3

import pygame

import Config
import DisplaySoftList
import WindowManager
import XmlGetter

Config.parse_command_line()

pygame.init()
main_window = pygame.display.set_mode((Config.desktop[2], Config.desktop[3]), flags=pygame.NOFRAME)
pygame.display.set_caption('RandoMame')
font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 32)
text = font.render('RandoMame', True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.center = (Config.desktop[2] // 2, Config.desktop[3] // 2)
main_window.blit(text, textRect)
pygame.display.update()

if Config.available_softlist is True:
    DisplaySoftList.display_soft_list()
    exit(0)

machine_list, soft_list = XmlGetter.get()

if machine_list is not None:
    print("MAME version: ", machine_list.attrib["build"])
    print(len(machine_list), " unique machines")

if soft_list is not None:
    print(len(soft_list), " softwares lists")


WindowManager.start(machine_list, soft_list, Config.windows_quantity)
