import getopt
import multiprocessing
import sys

mame_binary = ""
mode = "arcade"
windows_quantity = multiprocessing.cpu_count()
timeout = 300
desktop = None
allow_preliminary = False
selected_softlist = []
selected_soft = []
need_softlist = False
available_softlist = False
description = None
year_min = None
year_max = None
linear = False


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "aAd:D:hlLmpsS:T:t:w:y:Y:",
                                   ["arcade", "all", "description=", "softlist", "selected_softlist=", "help",
                                    "available_softlist", "timeout=", "desktop=",
                                    "allow_preliminary",
                                    "window=", "year_min=", "year_max=", "music", "selected_soft=",
                                    "linear"])
    except getopt.GetoptError:
        usage()

    global mode
    global selected_softlist
    global selected_soft
    global need_softlist
    global available_softlist
    global available_softlist
    global description
    global timeout
    global allow_preliminary
    global windows_quantity
    global year_min
    global year_max
    global desktop
    global linear

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
            selected_soft = arg.split(',')
        elif opt in ("-m", "--music"):
            mode = "music"
            windows_quantity = 1
            need_softlist = True
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
        elif opt in ("-w", "--window"):
            windows_quantity = int(arg)
        elif opt in ("-l", "--available_softlist"):
            available_softlist = True
        elif opt in ("-y", "--year_min"):
            year_min = int(arg)
        elif opt in ("-Y", "--year_max"):
            year_max = int(arg)
        elif opt in ("-L", "--linear"):
            linear = True
        else:
            print("Unknown option" + opt)
            usage()

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
        print("Preliminary drivers not allowed")

    if year_min is not None:
        print("No machines/softwares earlier than", year_min)
    if year_max is not None:
        print("No machines/softwares later than", year_max)

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
    print("  -s, --softlist : softlist mode: run only drivers using softwares (default)")
    print("  -A, --all : both arcade mode and softlist mode")
    print("  -S, --selected_softlist= : comma separated list of selected softlists which will be run")
    print("")
    print(" - FILTER")
    print("  -d, --description : coma separated regex expression filtering machines and softwares description")
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
    print("")
    print(" - OTHER")
    print("  -l, --available_softlist : display available softlists")
    print("  -h, --help : print this message")

    sys.exit(1)
