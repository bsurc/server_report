#!python3 -x
from server_report import *
import sys, getopt

def main(arguments):
    startdate = ''
    enddate = ''
    endpoint = ''
    try:
        opts, args = getopt.getopt(arguments, "hlE:ujs:e:a", ["help","list","endpoint=","users","jobs","start=","end=","active"])
    except getopt.GetoptError:
        print("report.py [-h|--help] [-l|--list] [-u|--users] [-j|--jobs] [-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
        sys.exit(1)
    if len(opts) == 0:
        print("report.py [-h|--help] [-l|--list] [-u|--users] [-j|--jobs] [-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("report.py [-h|--help] [-l|--list] [-u|--users] [-j|--jobs] [-a|--active] [-E <uuid>|--endpoint=<uuid>] [-s <isodate>|--start=<isodate>] [-e <isodate>|--end=<isodate>]")
            sys.exit(0)
        elif opt in ("-E", "--endpoint"):
            endpoint = arg
        elif opt in ("-s", "--start"):
            startdate = arg
        elif opt in ("-e", "--end"):
            enddate = arg
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
       main(sys.argv[1:])
