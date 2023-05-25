import Display
import FilterSoftware
from Item import Item


def generate_music_list(all_machine_xml, softlist_xml_list):
    found_music = []

    selected_softlist_xml = None
    for softlist_xml in softlist_xml_list.findall('softwarelist'):
        if softlist_xml.attrib['name'] == "vgmplay":
            selected_softlist_xml = softlist_xml
            break

    found_qty = 0

    for soft_xml in selected_softlist_xml:
        item = FilterSoftware.get(all_machine_xml, soft_xml)
        if item is None:
            continue

        for part_xml in item.get_soft_xml().findall('part'):
            part_item = Item(all_machine_xml)
            part_item.set_soft_xml(item.get_soft_xml())
            part_item.set_part_xml(part_xml)
            found_music.append(part_item)

        if len(found_music) > found_qty + 1000:
            found_qty = len(found_music)
            Display.print_text("Found " + str(len(found_music)) + " musics")

    return found_music
