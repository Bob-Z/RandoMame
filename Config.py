import getopt
import sys

mame_binary = ""
duration = 300


def parse_command_line():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "duration="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-d", "--duration"):
            global duration
            duration = arg
        else:
            usage()

    global mame_binary
    mame_binary = args[0]

    print("Configuration:")
    print("MAME binary:", mame_binary)
    print("Individual machine's run duration:", duration, "seconds")
    print("")


def usage():
    print("RandoMame [-d=<duration>] MAME_binary")
    print("")
    print("  MAME_binary : path to MAME's binary")
    print("  -d, --duration : individual run duration in seconds")
    print("")

    sys.exit(1)
