import FilterSoftware

def generate_music_list(soft_list_list):
    found_music = []

    selected_soft_list = None
    for soft_list in soft_list_list.findall('softwarelist'):
        if soft_list.attrib['name'] == "vgmplay":
            selected_soft_list = soft_list
            break

    for soft in selected_soft_list:
        soft_name, description = FilterSoftware.get(soft)
        if soft_name is None:
            continue

        for part in soft.findall('part'):
            feature = part.find('feature')
            found_music.append(
                ["vgmplay -quik " + soft_name + ":" + part.attrib['name'], feature.attrib['value'] + " // " + description])

    if len(found_music) > 0:
        print("Found", len(found_music), "musics")

    return found_music
