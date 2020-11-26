import re

import Config


def get(soft):
    soft_description = soft.find('description')

    if len(Config.selected_soft) > 0:
        found = False
        for driver_name in Config.selected_soft:
            if soft.attrib['name'] == driver_name:
                found = True
                break

        if found is False:
            return None, None

    if Config.description is not None:
        for desc in Config.description:
            found = False
            if re.match(desc, soft_description.text, re.IGNORECASE) is not None:
                found = True
                break

        if found is False:
            return None, None

    year = soft.find('year').text
    if Config.year_min is not None:
        try:
            if int(year) < Config.year_min:
                return None, None
        except ValueError:
            return None, None

    if Config.year_max is not None:
        try:
            if int(year) > Config.year_max:
                return None, None
        except ValueError:
            return None, None

    if soft.attrib['supported'] is not None:
        if soft.attrib['supported'] != "yes":
            return None, None

    description = soft_description.text + " (" + year + ")"

    return soft.attrib['name'], description
