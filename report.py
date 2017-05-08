#!python3 -x
from server_report import *
import sys, getopt

def main(arguments):
    try:
        opts, args = getopt.getopt(arguments, "hls:", ["help","list","stats="])
    except getopt.GetoptError:
        print("report.py [-h|--help] [-l|--list] [-s <uuid>|--stats=<uuid>]")
        sys.exit(1)
    if len(opts) == 0:
        print("report.py [-h|--help] [-l|--list] [-s <uuid>|--stats=<uuid>]")
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("report.py [-h|--help] [-l|--list] [-s <uuid>|--stats=<uuid>]")
            sys.exit(0)
        elif opt in ("-l", "--list"):
            list.list()
        elif opt in ("-s", "--stats"):
            list.list(arg)

if __name__ == "__main__":
       main(sys.argv[1:])
