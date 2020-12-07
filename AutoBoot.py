lib = {
    "pcecd": {
        "pce": ('pcecd.lua', 1),
        "tg16": ('pcecd.lua', 1),
        "sgx": ('pcecd.lua', 1)
    },

    "megacd": {
        "megacd": ('megacd.lua', 3),
        "32x_mcd": ('megacd.lua', 3),
        "megacd2": ('megacd.lua', 3),
        "megacda": ('megacd.lua', 3)
    },

    "megacdj": {
        "aiwamcd": ('megacd.lua', 3),
        "32x_mcdj": ('megacd.lua', 3),
        "laseractj": ('megacd.lua', 3),
        "megacd2j": ('megacd.lua', 3),
        "megacdj": ('megacd.lua', 3),
        "wmega": ('megacd.lua', 3),
        "wmegam2": ('megacd.lua', 3)
    },

    "segacd": {
        "32x_scd": ('megacd.lua', 3),
        "cdx": ('megacd.lua', 3),
        "laseract": ('megacd.lua', 3),
        "segacd": ('megacd.lua', 3),
        "segacd2": ('megacd.lua', 3),
        "xeye": ('megacd.lua', 3)
    },

    "cpc_cass": {
        "cpc464": ('cpc_cass.lua', 2),
        "cpc664": ('cpc_cass.lua', 2),
        "cpc6128": ('cpc_cass.lua', 2),
        "cpc6128s": ('cpc_cass.lua', 2),
        "cpc6128sp": ('cpc_cass.lua', 2),
        "cpc464p": ('cpc_cass.lua', 2),
        "cpc6128p": ('cpc_cass.lua', 2),
        "cpc6128f": ('cpc_cass.lua', 2),
        "kccomp": ('cpc_cass.lua', 2),
    },

    "ngp": {
        "ngp": ('ngp.lua', 0),
        "ngpc": ('ngp.lua', 0),
    },

    "ngpc": {
        "ngp": ('ngp.lua', 0),
        "ngpc": ('ngp.lua', 0),
    },

    "spectrum_cass": {
        "blitzs": ('spectrum_cass.lua', 2),
        "byte": ('spectrum_cass.lua', 2),
        "cip03": ('spectrum_cass.lua', 2),
        "compani1": ('spectrum_cass.lua', 2),
        "dgama87": ('spectrum_cass.lua', 2),
        "dgama88": ('spectrum_cass.lua', 2),
        "didaktk": ('spectrum_cass.lua', 2),
        "didakt90": ('spectrum_cass.lua', 2),
        "didakm91": ('spectrum_cass.lua', 2),
        "didakm92": ('spectrum_cass.lua', 2),
        "didakm93": ('spectrum_cass.lua', 2),
        "hc85": ('spectrum_cass.lua', 2),
        "hc90": ('spectrum_cass.lua', 2),
        "hc91": ('spectrum_cass.lua', 2),
        "hc128": ('spectrum_cass.lua', 2),
        "jet": ('spectrum_cass.lua', 2),
        "mistrum": ('spectrum_cass.lua', 2),
        "orizon": ('spectrum_cass.lua', 2),
        "scorpio": ('spectrum_cass_scorpio.lua', 0),
        "sintez2": ('spectrum_cass.lua', 2),
        "spectrum": ('spectrum_cass.lua', 2),
        "specpls2": ('spectrum_cass.lua', 2),
        "specpls3": ('spectrum_cass.lua', 2),
        "specpl3e": ('spectrum_cass.lua', 3),
        "spec128": ('spectrum_cass.lua', 2),
        "spec80k": ('spectrum_cass_spec80k.lua', 0),
        "spektrbk": ('spectrum_cass.lua', 2),
        "sp3eata": ('spectrum_cass.lua', 2),
        "sp3ezcf": ('spectrum_cass.lua', 2),
        "sp3e8bit": ('spectrum_cass.lua', 2),
        "pentagon": ('spectrum_cass.lua', 2),
        "pent1024": ('spectrum_cass_pent1024.lua', 0),
        "tc2048": ('spectrum_cass.lua', 2),
        "ts2068": ('spectrum_cass.lua', 2),
        "tk90x": ('spectrum_cass.lua', 2),
        "tk95": ('spectrum_cass.lua', 2),
        "uk2086": ('spectrum_cass.lua', 2),
    }
    # bk08
    # specide
    # cip01
}


def get_autoboot_command(soft_list_name, machine_name):
    try:
        return lib[soft_list_name][machine_name]
    except KeyError:
        return None, None
