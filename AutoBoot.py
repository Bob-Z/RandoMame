lib = [('pcecd', 'pce', 'pcecd_pce.lua', 1)]

lib = {
    "pcecd": {"pce": ('pcecd.lua', 1),
              "tg16": ('pcecd.lua', 1),
              "sgx": ('pcecd.lua', 1)},

    "megacd": {"megacd": ('megacd.lua', 3),
               "32x_mcd": ('megacd.lua', 3),
               "megacd2": ('megacd.lua', 3),
               "megacda": ('megacd.lua', 3)},

    "megacdj": {"aiwamcd": ('megacd.lua', 3),
                "32x_mcdj": ('megacd.lua', 3),
                "laseractj": ('megacd.lua', 3),
                "megacd2j": ('megacd.lua', 3),
                "megacdj": ('megacd.lua', 3),
                "wmega": ('megacd.lua', 3),
                "wmegam2": ('megacd.lua', 3)},

    "segacd": {"32x_scd": ('megacd.lua', 3),
               "cdx": ('megacd.lua', 3),
               "laseract": ('megacd.lua', 3),
               "segacd": ('megacd.lua', 3),
               "segacd2": ('megacd.lua', 3),
               "xeye": ('megacd.lua', 3)}
}


def get_autoboot_command(soft_list_name, machine_name):
    try:
        return lib[soft_list_name][machine_name]
    except KeyError:
        return None, None
