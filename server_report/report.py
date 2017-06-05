#!python3 -x
"""Driver method for server_report.

Functions:
main -- main method
"""
import server_report.func as func
import sys
import getopt
import logging


helpstring = ("report  [-h|--help] [-v|--verbose] "
              "[-d|--debug] [-l|--list]\n"
              "        [-u|--users] [-j|--jobs] [-a|--active] [-e|--error]\n"
              "        [-E <uuid>|--endpoint=<uuid>]\n"
              "        [--start=<isodate>]\n"
              "        [--end=<isodate>]")
shortops = "hlE:ujeavd"
longops = ["help", "list", "endpoint=", "users", "jobs", "start=",
           "end=", "active", "error", "verbose", "debug"]


def main():
    """Parse options and call appropriate method from func."""
    arguments = sys.argv[1:]
    startdate = ''
    enddate = ''
    endpoint = ''
    logging_level = logging.WARNING
    try:
        opts, args = getopt.getopt(arguments, shortops, longops)
    except getopt.GetoptError:
        print("{}".format(helpstring))
        sys.exit(1)
    if len(opts) == 0:
        print("{}".format(helpstring))
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("{}".format(helpstring))
            sys.exit(0)
        elif opt in ("-E", "--endpoint"):
            endpoint = arg
        elif opt in ("--start"):
            startdate = arg
        elif opt in ("--end"):
            enddate = arg
        elif opt in ("-v", "--verbose"):
            logging_level = logging.INFO
        elif opt in ("-d", "--debug"):
            logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level)
    for opt, arg in opts:
        if opt in ("-u", "--users"):
            func.user_frequency(endpoint, startdate, enddate)
        elif opt in ("-j", "--jobs"):
            func.job_count(endpoint, startdate, enddate)
        elif opt in ("-l", "--list"):
            func.list_endpoints()
        elif opt in ("-a", "--active"):
            func.running_count(endpoint)
        elif opt in ("-e", "--error"):
            func.errored_jobs(endpoint, startdate, enddate)


if __name__ == "__main__":
    main()
