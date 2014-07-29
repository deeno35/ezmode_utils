#!/usr/bin/env python
#################################################
# Description: Run a shell command and timeout if it runs longer than X seconds
#
# Author: d_k_nguyen@yahoo.com
# Date: 07/27/2014
#

import getopt
import sys
import signal
import subprocess


def usage():
    print "USAGE: %s -c <command_name -t <timeout>", sys.argv[0]
    print "-c full shell command to run.  Quote it if it contains spaces"
    print "-t timeout in seconds (default: 60)\n\n"
    sys.exit(3)

def parse_args():
    """
    Returns a dict of the args as it's easier to work with than a list of
    tuples.
    """
    return_dict = {"timeout" : 60}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:t:",
                                    ["command=", "timeout="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-c", "--command"):
            return_dict["command"] = str(arg)
        elif opt in ("-t", "--timeout"):
            return_dict["timeout"] = int(arg)

    # Arg enforcement
    if "command" not in return_dict:
        print "ERROR: -c <command> is a required arg\n\n"
        usage()

    return return_dict

def alarm_handler(signum, frame):
    print 'Signal handler called with signal', signum
    print "Timeout Reached, exiting abnormally"
    sys.exit(3)


if __name__ == '__main__':
    args = parse_args()

    #create the timer
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(args["timeout"])
    # run the command
    subprocess.call(args["command"], shell=True)
    # unset the timer if the command completes before time is up
    signal.alarm(0)
