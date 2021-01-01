import getopt
import multiprocessing
import sys

mame_binary = ""
mode = "arcade"
windows_quantity = multiprocessing.cpu_count()
timeout = 300
desktop = None
allow_preliminary = False
allow_not_supported = False
selected_softlist = []
selected_soft = []
need_machine = True
need_softlist = False
available_softlist = False
description = None
year_min = None
year_max = None
linear = False
auto_quit = False
smart_sound_timeout_sec = 1
manufacturer = None
ini_file = None
include = None
exclude = None
extra = None
force_driver = None
loose_search = False


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "aAd:D:E:f:hi:I:lLmM:noO:pqsS:T:t:w:x:y:Y:",
                                   ["arcade", "all", "description=", "softlist", "selected_softlist=", "help",
                                    "available_softlist", "timeout=", "desktop=",
                                    "allow_preliminary",
                                    "window=", "year_min=", "year_max=", "music", "selected_soft=",
                                    "allow_not_supported",
                                    "linear", "quit", "smart_sound_timeout", "manufacturer=", "ini_file=", "include=",
                                    "exclude=", "extra=", "force_driver=", "loose_search"])
    except getopt.GetoptError:
        usage()

    global mode
    global selected_softlist
    global selected_soft
    global need_softlist
    global need_machine
    global available_softlist
    global available_softlist
    global description
    global timeout
    global allow_preliminary
    global allow_not_supported
    global windows_quantity
    global year_min
    global year_max
    global desktop
    global linear
    global auto_quit
    global smart_sound_timeout_sec
    global manufacturer
    global ini_file
    global include
    global exclude
    global extra
    global force_driver
    global loose_search

    for opt, arg in opts:
        if opt in ("-a", "--arcade"):
            mode = "arcade"
        elif opt in ("-A", "--all"):
            mode = "all"
            need_softlist = True
        elif opt in ("-d", "--description"):
            description = arg.split(':::')
            need_softlist = True
        elif opt in ("-s", "--softlist"):
            mode = "softlist"
            need_softlist = True
        elif opt in ("-S", "--selected_softlist"):
            mode = "selected softlist"
            selected_softlist = arg.split(',')
            need_softlist = True
        elif opt in ("-T", "--selected_soft"):
            selected_soft = arg
        elif opt in ("-m", "--music"):
            mode = "music"
            windows_quantity = 1
            need_machine = False
            need_softlist = True
            smart_sound_timeout_sec = 0
        elif opt in ("-t", "--timeout"):
            timeout = int(arg)
        elif opt in ("-D", "--desktop"):
            desktop = arg.split('x')
            desktop[0] = int(desktop[0])
            desktop[1] = int(desktop[1])
            desktop[2] = int(desktop[2])
            desktop[3] = int(desktop[3])
        elif opt in ("-h", "--help"):
            usage()
        elif opt in ("-p", "--allow_preliminary"):
            allow_preliminary = True
        elif opt in ("-n", "--allow_not_supported"):
            allow_not_supported = True
        elif opt in ("-o", "--loose_search"):
            loose_search = True
        elif opt in ("-O", "--smart_sound_timeout"):
            smart_sound_timeout_sec = int(arg)
        elif opt in ("-w", "--window"):
            windows_quantity = int(arg)
        elif opt in ("-l", "--available_softlist"):
            available_softlist = True
        elif opt in ("-y", "--year_min"):
            year_min = int(arg)
        elif opt in ("-M", "--manufacturer"):
            manufacturer = arg
        elif opt in ("-Y", "--year_max"):
            year_max = int(arg)
        elif opt in ("-L", "--linear"):
            linear = True
        elif opt in ("-q", "--quit"):
            auto_quit = True
        elif opt in ("-i", "--ini_file"):
            ini_file = arg
        elif opt in ("-I", "--include"):
            include = arg
        elif opt in ("-E", "--exclude"):
            exclude = arg
        elif opt in ("-x", "--extra"):
            extra = arg
        elif opt in ("-f", "--force_driver"):
            force_driver = arg
        else:
            print("Unknown option " + opt)
            usage()

    if windows_quantity == 1:
        smart_sound_timeout_sec = 0

    global mame_binary
    mame_binary = args[0]

    print("Configuration:")
    mode_str = "Mode: " + mode
    if len(selected_softlist) > 0:
        mode_str += " with "
        for s in selected_softlist:
            mode_str += s + " "
    print(mode_str)
    print("MAME binary:", mame_binary)
    print("Simultaneous windows :", windows_quantity)
    print("Individual machine's run timeout:", str(timeout), "seconds")
    print("Desktop geometry", desktop)
    if allow_preliminary is True:
        print("Preliminary drivers allowed")
    else:
        print("Preliminary drivers disallowed")

    if allow_not_supported is True:
        print("Not supported softwares allowed")
    else:
        print("Not supported softwares disallowed")

    if year_min is not None:
        print("No machines/softwares earlier than", year_min)
    if year_max is not None:
        print("No machines/softwares later than", year_max)

    if manufacturer is not None:
        print("Manufacturer: ", manufacturer)

    if ini_file is not None:
        print("ini file: ", ini_file)
    if include is not None:
        print("included sections: ", include)
    if exclude is not None:
        print("excluded sections: ", exclude)

    if extra is not None:
        print("extra command: ", extra)

    if force_driver is not None:
        print("forced driver: ", force_driver)

    if loose_search is True:
        print("Loose description search enabled")

    if smart_sound_timeout_sec > 0:
        print("Smart sound timeout =", smart_sound_timeout_sec, "seconds")
    else:
        print("Smart sound disabled")

    print("")


def usage():
    print("RandoMame [options] MAME_binary")
    print("")
    print("  MAME_binary : path to MAME's binary")
    print("")
    print("options:")
    print("=========")
    print("")
    print(" - MODE")
    print("  -a, --arcade : arcade mode: run only coins operated machine (default)")
    print("  -A, --all : both arcade mode and softlist mode")
    print("  -s, --softlist : softlist mode: run only drivers using softwares (default)")
    print("  -S, --selected_softlist= : comma separated list of selected softlists which will be run")
    print("  -m, --music : video game music mode")
    print("")
    print(" - FILTER")
    print("  -d, --description : coma separated regex expression filtering machines and softwares description")
    print("  -E, --exclude= : coma separated sections from ini file excluded")
    print("  -f, --force_driver= : coma separated list of drivers used")
    print("  -i, --ini_file= : ini file from where sections will be included or excluded")
    print("  -I, --include= : coma separated sections from ini file included ")
    print("  -M, --manufacturer : coma separated list of manufacturer allowed")
    print("  -n, --allow_not_supported : Allow not supported softwares")
    print("  -o, --loose_search : Enable loose description search for machine name. Default is strict search")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("  -T, --selected_soft= : Coma separated list of allowed driver names (use with selected_softlist mode)")
    print("  -x, --extra= : extra command passed to MAME binary")
    print("  -y, --year_min= : Machines/softwares can't be earlier than this")
    print("  -Y, --year_max= : Machines/softwares can't be older than this")
    print("")
    print(" - APPEARANCE")
    print("  -w, --window= : simultaneous windows quantity")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("  -t, --timeout= : individual run timeout in seconds")
    print("  -L, --linear= : choose selected machines/softwares in MAME's list order (default is random)")
    print("  -q, --quit : Quit when all selected machines/softwares have been shown (default never quit)")
    print(
        "  -O, --smart_sound_timeout : Only one window is unmuted. After smart_sound_timeout seconds of silence, another window is un-muted. Set this to 0 to deactivate smart-sound")
    print("")
    print(" - OTHER")
    print("  -l, --available_softlist : display available softlists")
    print("  -h, --help : print this message")

    sys.exit(1)
