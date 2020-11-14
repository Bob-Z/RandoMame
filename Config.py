import getopt
import multiprocessing
import sys

mame_binary = ""
mode = "arcade"
windows_quantity = multiprocessing.cpu_count()
duration = 300
desktop = None
allow_preliminary = False


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ashd:D:pw:",
                                   ["arcade", "softlist", "help", "duration=", "desktop=", "allow_preliminary",
                                    "window="])
    except getopt.GetoptError:
        usage()

    global mode
    for opt, arg in opts:
        if opt in ("-a", "--arcade"):
            mode = "arcade"
        elif opt in ("-s", "--softlist"):
            mode = "softlist"
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
        else:
            usage()

    global mame_binary
    mame_binary = args[0]

    print("Configuration:")
    print("Mode: " + mode)
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
    print("  -d, --duration= : individual run duration in seconds")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("  -h, --help : print this message")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("  -w, --window= : simultaneous windows quantity")
    print("")

    sys.exit(1)
