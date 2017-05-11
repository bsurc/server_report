#!python3 -x
import server_report.func as func
import sys
import getopt
import logging


def main():
    arguments = sys.argv[1:]
    startdate = ''
    enddate = ''
    endpoint = ''
    loggingLevel = logging.WARNING
    try:
        opts, args = getopt.getopt(arguments, "hlE:ujs:e:avd", ["help","list","endpoint=","users","jobs","start=","end=","active","verbose","debug"])
    except getopt.GetoptError:
        print("report \t[-h|--help] [-v|--verbose] [-d|--debug] [-l|--list] [-u|--users] [-j|--jobs]\n\t[-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
        sys.exit(1)
    if len(opts) == 0:
        print("report \t[-h|--help] [-v|--verbose] [-d|--debug] [-l|--list] [-u|--users] [-j|--jobs]\n\t[-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("report \t[-h|--help] [-v|--verbose] [-d|--debug] [-l|--list] [-u|--users] [-j|--jobs]\n\t[-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
            sys.exit(0)
        elif opt in ("-E", "--endpoint"):
            endpoint = arg
        elif opt in ("-s", "--start"):
            startdate = arg
        elif opt in ("-e", "--end"):
            enddate = arg
        elif opt in ("-v", "--verbose"):
            loggingLevel = logging.INFO
        elif opt in ("-d", "--debug"):
            loggingLevel = logging.DEBUG
    logging.basicConfig(level=loggingLevel)
    for opt, arg in opts:
        if opt in ("-u", "--users"):
            func.user_frequency(endpoint,startdate,enddate)
        elif opt in ("-j", "--jobs"):
            func.job_count(endpoint,startdate,enddate)
        elif opt in ("-l", "--list"):
            func.list_endpoints()
        elif opt in ("-a", "--active"):
            func.running_count(endpoint)


if __name__ == "__main__":
       main()
