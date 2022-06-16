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
no_manufacturer = None
ini_file = None
include = None
exclude = None
extra = None
force_driver = None
loose_search = False
multi_search = False
start_command = None
end_command = None
final_command = None
record = None
title_text = None
title_background = None
dry_run = False
source_file = None
no_clone = False
no_soft_clone = False
device = None
slot_option = None
display_min = None
end_text = None
end_background = None
end_duration = None
check = None
sort_by_name = False
sort_by_year = False
sort_reverse = False
emulation_time = False
prefer_parent = False


def parse_command_line():
    opts, args = getopt.getopt(sys.argv[1:],
                               "aAb:B:c:C:d:D:eE:f:F:g:G:hH:i:I:jJk:KlLmM:NnoO:pPqQ:rRsS:T:t:uUvVw:X:x:y:Y:z:Z:",
                               ["arcade", "all", "description=", "softlist", "selected_softlist=", "help",
                                "available_softlist", "timeout=", "desktop=",
                                "allow_preliminary",
                                "window=", "year_min=", "year_max=", "music", "selected_soft=",
                                "allow_not_supported",
                                "linear", "quit", "smart_sound_timeout", "manufacturer=", "ini_file=", "include=",
                                "exclude=", "extra=", "force_driver=", "loose_search", "multi_search", "start_command=",
                                "end_command=", "record=", "title_text=", "title_bg=", "dry_run", "source_file=",
                                "no_clone", "device=", "slot_option=", "display_min=", "end_text=", "end_bg=",
                                "end_duration=", "check=",
                                "sort_by_name", "sort_by_year", "sort_reverse",
                                "emulation_time", "final_command=", "no_manufacturer=", "standalone", "slotmachine",
                                "no_soft_clone", "prefer_parent"])

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
    global no_manufacturer
    global ini_file
    global include
    global exclude
    global extra
    global force_driver
    global loose_search
    global multi_search
    global start_command
    global end_command
    global final_command
    global record
    global title_text
    global title_background
    global dry_run
    global source_file
    global no_clone
    global no_soft_clone
    global device
    global slot_option
    global display_min
    global end_text
    global end_background
    global end_duration
    global check
    global sort_by_name
    global sort_by_year
    global sort_reverse
    global emulation_time
    global prefer_parent

    for opt, arg in opts:
        if opt in ("-a", "--arcade"):
            mode = "arcade"
        elif opt in ("-u", "--standalone"):
            mode = "standalone"
        elif opt in ("-U", "--slotmachine"):
            mode = "slotmachine"
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
        elif opt in ("-V", "--multi_search"):
            multi_search = True
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
        elif opt in ("-H", "--no_manufacturer"):
            no_manufacturer = arg
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
        elif opt in ("-X", "--final_command"):
            final_command = arg
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
        elif opt in ("-K", "--no_soft_clone"):
            no_soft_clone = True
        elif opt in ("-b", "--device"):
            device = arg.split(',')
        elif opt in ("-B", "--slot_option"):
            slot_option = arg.split(',')
        elif opt in ("-Q", "--display_min"):
            display_min = int(arg)
        elif opt in ("-z", "--end_text"):
            end_text = arg.split(':::')
        elif opt in ("-Z", "--end_bg"):
            end_background = arg
        elif opt in ("-d", "--end_duration"):
            end_duration = int(arg)
        elif opt in ("-k", "--check"):
            check = arg
            need_softlist = True
        elif opt in ("-j", "--sort_by_name"):
            sort_by_name = True
        elif opt in ("-J", "--sort_by_year"):
            sort_by_year = True
        elif opt in ("-v", "--sort_reverse"):
            sort_reverse = True
        elif opt in ("-e", "--emulation_time"):
            emulation_time = True
        elif opt in ("-P", "--prefer_parent"):
            prefer_parent = True
        else:
            print("Unknown option ", opt)
            usage()

    if windows_quantity == 1:
        smart_sound_timeout_sec = 0

    if sort_by_year is True or sort_by_name is True:
        linear = True

    global mame_binary
    mame_binary = args[0]

    print("")
    print("")
    print("Configuration:")
    print("MAME binary:", mame_binary)
    if check is not None:
        print("Check path:", check)
    else:
        mode_str = "Mode: " + mode
        if len(selected_softlist) > 0:
            mode_str += " with "
            for s in selected_softlist:
                mode_str += s + " "
        print(mode_str)
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

        if no_manufacturer is not None:
            print("Manufacturer forbidden: ", no_manufacturer)

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

        if multi_search is True:
            print("Multiple search enabled")

        if smart_sound_timeout_sec > 0:
            print("Smart sound timeout =", smart_sound_timeout_sec, "seconds")
        else:
            print("Smart sound disabled")

        if source_file is not None:
            print("source files allowed: ", source_file)

        if no_clone is True:
            print("No clones allowed")

        if no_soft_clone is True:
            print("No software clones allowed")

        if prefer_parent is True:
            print("Prefer parent")

        if device is not None:
            print("device allowed: ", device)

        if slot_option is not None:
            print("slot option allowed: ", slot_option)

        if display_min is not None:
            print("Minimum display quantity allowed: ", display_min)

        if sort_by_name is True:
            print("Sort by name")

        if sort_by_year is True:
            print("Sort by year")

        if sort_reverse is True:
            print("Sort reverse")

        if emulation_time is True:
            print("Using emulation time for timeout")

        if start_command is not None:
            print("Start command: ", start_command)

        if end_command is not None:
            print("End command: ", end_command)

        if final_command is not None:
            print("Final command: ", final_command)

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
    print("  -a, --arcade : Run only coins operated machine without slot machines (default)")
    print("  -A, --all : all machines")
    print("  -u, --standalone : Run stand alone machines (no coins, no payout, no additional software)")
    print("  -U, --slotmachine : Run slot machines")
    print("  -s, --softlist : softlist mode: run only drivers using softwares")
    print("  -S, --selected_softlist= : comma separated list of selected softlists which will be run")
    print("  -m, --music : video game music mode")
    print("  -c, --check= : check files in given path")
    print("")
    print(" - FILTER")
    print("  -b, --device= : coma separated list of names of allowed devices")
    print("  -B, --slot_option= : coma separated list of names of allowed slot_option")
    print(
        "  -d, --description= : coma separated list of regex expression filtering machines and softwares description. Use ^desc$ for exact match")
    print("  -E, --exclude= : coma separated list of sections from ini file excluded")
    print("  -f, --force_driver= : coma separated list of drivers used")
    print("  -F, --source_file= : coma separated list of source file allowed")
    print("  -H, --no_manufacturer : coma separated list of forbidden manufacturers")
    print("  -i, --ini_file= : ini file from where sections will be included or excluded")
    print("  -I, --include= : coma separated sections from ini file included ")
    print("  -K, --no_soft_clone : do not allow clone software")
    print("  -M, --manufacturer : coma separated list of allowed manufacturers")
    print("  -N, --no_clone : do not allow clone machines")
    print("  -n, --allow_not_supported : Allow not supported softwares")
    print("  -o, --loose_search : Enable loose description search for machine name. Default is strict search")
    print("  -V, --multi_search : Enable multiple machines to be selected by their description. Default is only on e machine selected")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("  -P, --prefer_parent : When selecting a machine for a software, prefer parent rather than clones")
    print("  -Q, --display_min= : Minimum displays quantity allowed")
    print(
        "  -T, --selected_soft= : Coma separated list of allowed software (short) names (use with selected_softlist mode)")
    print("  -y, --year_min= : Machines/softwares can't be earlier than this")
    print("  -Y, --year_max= : Machines/softwares can't be older than this")
    print("")
    print(" - APPEARANCE")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("  -e, --emulation_time : Use emulation time rather than real life time for timeout")
    print("  -L, --linear= : choose selected machines/softwares in MAME's list order (default is random)")
    print("  -j, --sort_by_name : Sort machines/software by name")
    print("  -J, --sort_by_year : Sort machines/software by year")
    print("  -q, --quit : Quit when all selected machines/softwares have been shown (default never quit)")
    print("  -t, --timeout= : individual run timeout in seconds")
    print("  -v, --sort_reverse : Reverse sorting")
    print("  -w, --window= : simultaneous windows quantity")
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
    print("  -C, --end_command= : command line to be executed at end (when there is nothing more to be displayed)")
    print("  -X, --final_command= : command line to be executed at end (just before RandoMame exits)")
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
