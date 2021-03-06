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
start_command = None
end_command = None
record = None
title_text = None
title_background = None
dry_run = False
source_file = None
no_clone = False
device = None
end_text = None
end_background = None
end_duration = None


def parse_command_line():
    opts, args = getopt.getopt(sys.argv[1:], "aAb:c:C:d:d:D:E:f:F:g:G:hi:I:lLmM:NnoO:pqrRsS:T:t:w:x:y:Y:z:Z:",
                               ["arcade", "all", "description=", "softlist", "selected_softlist=", "help",
                                "available_softlist", "timeout=", "desktop=",
                                "allow_preliminary",
                                "window=", "year_min=", "year_max=", "music", "selected_soft=",
                                "allow_not_supported",
                                "linear", "quit", "smart_sound_timeout", "manufacturer=", "ini_file=", "include=",
                                "exclude=", "extra=", "force_driver=", "loose_search", "start_command=",
                                "end_command=", "record=", "title_text=", "title_bg=", "dry_run", "source_file=",
                                "no_clone", "device=", "end_text=", "end_bg=", "end_duration="])

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
    global start_command
    global end_command
    global record
    global title_text
    global title_background
    global dry_run
    global source_file
    global no_clone
    global device
    global end_text
    global end_background
    global end_duration

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
        elif opt in ("-c", "--start_command"):
            start_command = arg
        elif opt in ("-C", "--end_command"):
            end_command = arg
        elif opt in ("-r", "--record"):
            record = arg
        elif opt in ("-R", "--dry_run"):
            dry_run = True
        elif opt in ("-g", "--title_text"):
            title_text = arg.split(':::')
        elif opt in ("-G", "--title_bg"):
            title_background = arg
        elif opt in ("-F", "--source_file"):
            source_file = arg
        elif opt in ("-N", "--no_clone"):
            no_clone = True
        elif opt in ("-b", "--device"):
            device = arg
        elif opt in ("-z", "--end_text"):
            end_text = arg.split(':::')
        elif opt in ("-Z", "--end_bg"):
            end_background = arg
        elif opt in ("-d", "--end_duration"):
            end_duration = int(arg)
        else:
            print("Unknown option ", opt)
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

    if source_file is not None:
        print("source files allowed: ", source_file)

    if no_clone is True:
        print("No clones allowed")

    if device is not None:
        print("device allowed: ", device)

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
    print("  -s, --softlist : softlist mode: run only drivers using softwares")
    print("  -S, --selected_softlist= : comma separated list of selected softlists which will be run")
    print("  -m, --music : video game music mode")
    print("")
    print(" - FILTER")
    print("  -b, --device= : coma separated names of allowed devices")
    print("  -d, --description= : coma separated regex expression filtering machines and softwares description")
    print("  -E, --exclude= : coma separated sections from ini file excluded")
    print("  -f, --force_driver= : coma separated list of drivers used")
    print("  -F, --source_file= : coma separated list of source file allowed")
    print("  -i, --ini_file= : ini file from where sections will be included or excluded")
    print("  -I, --include= : coma separated sections from ini file included ")
    print("  -M, --manufacturer : coma separated list of manufacturer allowed")
    print("  -N, --no_clone : do not allow clone drivers")
    print("  -n, --allow_not_supported : Allow not supported softwares")
    print("  -o, --loose_search : Enable loose description search for machine name. Default is strict search")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("  -T, --selected_soft= : Coma separated list of allowed driver names (use with selected_softlist mode)")
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
    print("  -g, --title_text= : Display text at start (may be ':::' separated texts")
    print("  -G, --title_bg= : Display given image file at start")
    print("  -z, --end_text= : Display text at end (may be ':::' separated texts")
    print("  -Z, --end_bg= : Display given image file at end")
    print("  -d, --end_duration= : Display end duration in seconds")
    print("  -R, --dry_run= : Do not launch MAME (testing purpose only)")
    print("")
    print(" - OTHER")
    print("  -c, --start_command= : command line to be executed on start (when MAME is first launched)")
    print("  -C, --end_command= : command line to be executed at end (when Randomame window is closed)")
    print("  -l, --available_softlist : display available softlists")
    print("  -r, --record= : directory where session is recorded")
    print("  -x, --extra= : extra command passed to MAME binary")
    print("  -h, --help : print this message")

    sys.exit(1)


def allow_all():
    global allow_preliminary
    global allow_not_supported

    allow_preliminary = True
    allow_not_supported = True


def get_allowed_string():
    global allow_preliminary
    global allow_not_supported

    if allow_preliminary is True or allow_not_supported is True:
        allowed = " ("
        if allow_preliminary is True:
            allowed = allowed + "Preliminary"

        if allow_preliminary is True and allow_not_supported is True:
            allowed = allowed + " and "

        if allow_not_supported is True:
            allowed = allowed + "Not Supported"

        allowed = allowed + " allowed)"

        return allowed

    else:
        return " (No preliminary, no not supported)"
