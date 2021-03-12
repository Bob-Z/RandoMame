import Display
import FilterSoftware


def generate_music_list(soft_list_list):
    found_music = []

    selected_soft_list = None
    for soft_list in soft_list_list.findall('softwarelist'):
        if soft_list.attrib['name'] == "vgmplay":
            selected_soft_list = soft_list
            break

    found_qty = 0

    for soft in selected_soft_list:
        item = FilterSoftware.get(soft)
        if item is None:
            continue

        for part in item.get_soft_xml().findall('part'):
            item.set_part_xml(part)
            found_music.append(item)

        if len(found_music) > found_qty + 1000:
            found_qty = len(found_music)
            Display.print_text("Found " + str(len(found_music)) + " musics")

    return found_music
