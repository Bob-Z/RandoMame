import getopt
import sys

mame_binary = ""
duration = 300
desktop = None

def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:D:", ["help", "duration=", "desktop="])
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
        else:
            usage()

    global mame_binary
    mame_binary = args[0]

    print("Configuration:")
    print("MAME binary:", mame_binary)
    print("Individual machine's run duration:", duration, "seconds")
    print("Desktop geometry", desktop)
    print("")


def usage():
    print("RandoMame [-d=<duration>] MAME_binary")
    print("")
    print("  MAME_binary : path to MAME's binary")
    print("  -d, --duration= : individual run duration in seconds")
    print("  -D, --desktop= : desktop geometry in the form POSXxPOSYxWIDTHxHEIGHT, e.g. 0x0x1920x1080")
    print("")

    sys.exit(1)
