import re

import Config
from Item import Item


def get(soft_xml):
    item = Item()
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
                # Exact match
                s = "^" + desc + "$"
                if re.search(s, item.get_soft_description(), re.IGNORECASE) is not None:
                    found = True
                    break
            else:
                # Loose match
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

    return item
