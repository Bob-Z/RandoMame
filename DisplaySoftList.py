import XmlGetter


def display_soft_list():
    soft_list = XmlGetter.get_soft_list()

    for softlist in soft_list.findall("softwarelist"):
        print(softlist.attrib['name'], "-", softlist.attrib['description'], "-", len(softlist), "entries")
