import getopt
import sys
import multiprocessing

mame_binary = ""
windows_quantity = multiprocessing.cpu_count()
duration = 300
desktop = None
allow_preliminary = False


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:D:pw:", ["help", "duration=", "desktop=", "allow_preliminary", "window="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-d", "--duration"):
            global duration
            duration = arg
        elif opt in ("-D", "--desktop"):
            global desktop
            desktop = arg
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
    print("MAME binary:", mame_binary)
    print("Simultaneous windows :", windows_quantity)
    print("Individual machine's run duration:", duration, "seconds")
    print("Desktop geometry", desktop)
    print("Preliminary driver allowed :", allow_preliminary)
    print("")


def usage():
    print("RandoMame [-d=<duration>] MAME_binary")
    print("")
    print("  MAME_binary : path to MAME's binary")
    print("  -w, --window= : simultaneous windows quantity")
    print("  -d, --duration= : individual run duration in seconds")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("  -p, --allow_preliminary : Allow preliminary drivers")
    print("")

    sys.exit(1)
