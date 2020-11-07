import getopt
import sys

mame_binary = ""


def parse_command_line():
    try:
        # opts, args = getopt.getopt(sys.argv, "hg:d", ["help", "grammar="])
        opts, args = getopt.getopt(sys.argv, "h", ["help"])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        # elif opt == '-d':
        #    global _debug
        #    _debug = 1
        # elif opt in ("-g", "--grammar"):
        #    grammar = arg

    if len(args) < 2:
        usage()

    global mame_binary
    mame_binary = args[1]

    print("Configuration:")
    print("MAME binary:", mame_binary)
    print("")

def usage():
    print("RandoMame MAME_binary")
    print("")
    print(" - MAME_binary : path to MAME's binary")
    print("")

    sys.exit(1)
