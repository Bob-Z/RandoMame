import re

import Config
from Item import Item


def get(all_machine_xml, soft_xml):
    item = Item(all_machine_xml)
    item.set_soft_xml(soft_xml)

    if len(Config.selected_soft) > 0:
        found = False
        for soft_name in Config.selected_soft:
            if soft_xml.attrib['name'] == soft_name:
                found = True
                break

        if found is False:
            return None

    if Config.description is not None:
        for desc in Config.description:
            found = False

            if Config.loose_search is False:
                # For exact match (no more no less) : s = "^" + desc + "$"
                if re.search(desc, item.get_soft_description(), re.IGNORECASE) is not None:
                    found = True
                    break
            else:
                # Loose match
                # re.match start at string beginning
                if re.match(desc, item.get_soft_description(), re.IGNORECASE) is not None:
                    found = True
                    break

        if found is False:
            return None

    if Config.year_min is not None:
        try:
            if int(item.get_soft_year()) < Config.year_min:
                return None
        except ValueError:
            return None

    if Config.year_max is not None:
        try:
            if int(item.get_soft_year()) > Config.year_max:
                return None
        except ValueError:
            return None

    if Config.allow_not_supported is False:
        if soft_xml.attrib['supported'] is not None:
            if soft_xml.attrib['supported'] != "yes":
                return None

    if Config.no_soft_clone is True and "cloneof" in soft_xml.attrib:
        return None

    if Config.publisher is not None:
        publisher_found = False
        complete_soft_publisher = item.get_soft_publisher()
        for config_publisher in Config.publisher.split(","):
            if complete_soft_publisher.lower().find(config_publisher.lower()) != -1:
                publisher_found = True
                break
        if publisher_found is False:
            return None

    return item
