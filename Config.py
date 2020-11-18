import getopt
import multiprocessing
import sys

mame_binary = ""
mode = "arcade"
windows_quantity = multiprocessing.cpu_count()
duration = 300
desktop = None
allow_preliminary = False
selected_softlist = []
need_softlist = False
available_softlist = False;


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "aAd:D:hlpsS:w:",
                                   ["arcade", "all", "softlist", "selected_softlist=", "help", "available_softlist", "duration=", "desktop=",
                                    "allow_preliminary",
                                    "window="])
    except getopt.GetoptError:
        usage()

    global mode
    global selected_softlist
    global need_softlist

    for opt, arg in opts:
        if opt in ("-a", "--arcade"):
            mode = "arcade"
        elif opt in ("-A", "--all"):
            mode = "all"
            need_softlist = True
        elif opt in ("-s", "--softlist"):
            mode = "softlist"
            need_softlist = True
        elif opt in ("-S", "--selected_softlist"):
            mode = "selected softlist"
            selected_softlist = arg.split(',')
            need_softlist = True
        elif opt in ("-d", "--duration"):
            global duration
            duration = arg
        elif opt in ("-D", "--desktop"):
            global desktop
            desktop = arg
        elif opt in ("-h", "--help"):
            usage()
        elif opt in ("-p", "--allow_preliminary"):
            global allow_preliminary
            allow_preliminary = True
        elif opt in ("-w", "--window"):
            global windows_quantity
            windows_quantity = int(arg)
        elif opt in ("-l", "--available_softlist"):
            global available_softlist
            available_softlist = True
        else:
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
    print("Individual machine's run duration:", duration, "seconds")
    print("Desktop geometry", desktop)
    if allow_preliminary is True:
        print("Preliminary drivers allowed")
    else:
        print("Preliminary drivers not allowed")
    print("")


def usage():
    print("RandoMame [options] MAME_binary")
    print("")
    print("  MAME_binary : path to MAME's binary")
    print("")
    print("options:")
    print("=========")
    print("")
    print("  -a, --arcade : arcade mode: run only coins operated machine (default)")
    print("  -s, --softlist : softlist mode: run only drivers using softwares (default)")
    print("  -A, --all : both arcade mode and softlist mode")
    print("  -S, --selected_softlist= : comma separated list of selected softlists which will be run")
    print("  -d, --duration= : individual run duration in seconds")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("  -h, --help : print this message")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("  -w, --window= : simultaneous windows quantity")
    print("")

    sys.exit(1)
