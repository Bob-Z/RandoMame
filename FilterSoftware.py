import re

import Config


def get(soft):
    soft_description = soft.find('description')

    if Config.description is not None:
        if re.match(Config.description, soft_description.text, re.IGNORECASE) is None:
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
