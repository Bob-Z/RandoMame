lib = [('pcecd', 'pce', 'pcecd_pce.lua', 1)]

lib = {
    "pcecd": {"pce": ('pcecd.lua', 1),
              "tg16": ('pcecd.lua', 1),
              "sgx": ('pcecd.lua', 1)},

    "megacd": {"megacd": ('megacd.lua', 1),
               "32x_mcd": ('megacd.lua', 1),
               "megacd2": ('megacd.lua', 1),
               "megacda": ('megacd.lua', 1)},

    "megacdj": {"aiwamcd": ('megacd.lua', 1),
                "32x_mcdj": ('megacd.lua', 1),
                "laseractj": ('megacd.lua', 1),
                "megacd2j": ('megacd.lua', 1),
                "megacdj": ('megacd.lua', 1),
                "wmega": ('megacd.lua', 1),
                "wmegam2": ('megacd.lua', 1)},

    "segacd": {"32x_scd": ('megacd.lua', 1),
               "cdx": ('megacd.lua', 1),
               "laseract": ('megacd.lua', 1),
               "segacd": ('megacd.lua', 1),
               "segacd2": ('megacd.lua', 1),
               "xeye": ('megacd.lua', 1)}
}


def get_autoboot_command(soft_list_name, machine_name):
    try:
        return lib[soft_list_name][machine_name]
    except KeyError:
        return None, None
