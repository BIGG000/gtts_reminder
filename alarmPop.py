#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import shelve
import argparse
import datetime
from time import sleep
from subprocess import call
from datetime import timedelta
from datetime import datetime as dt
SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
alarms = shelve.open(SCRIPT_PATH + "/" + "alarms.dat")
print("Started @ ", str(dt.now()))


def run():
    print(alarms.keys())
    if len(alarms.keys()):
        alarms_list = sorted(alarms)
        while len(alarms_list):
            if str(dt.now()).replace(" ","-") >= alarms_list[0]:
                if alarms[alarms_list[0]] is not None:
                    call(["notify-send",
                          "-i",
                          SCRIPT_PATH + "/" + "event.png",
                          "Event!",
                          alarms[alarms_list[0]]]
                         )
                    if os.path.isfile(SCRIPT_PATH + "/" + alarms_list[0] + ".mp3"):
                        try:
                            call(["mpg321", "-q", "--stereo", SCRIPT_PATH + "/" + alarms_list[0] + ".mp3"])
                            os.remove(SCRIPT_PATH + "/" + alarms_list[0] + ".mp3")
                        except OSError:
                            print("Error playing audio! Make sure you have 'mpg321' installed!")
                else:
                    try:
                        call(["notify-send",
                              "-i",
                              SCRIPT_PATH + "/" + "alarm.png",
                              "Alarm!",
                              "You have an alarm set for now!"]
                             )
                        call(["mpg321", "-q", "--stereo", SCRIPT_PATH + "/" + "alarm.mp3"])
                        call(["mpg321", "-q", "--stereo", SCRIPT_PATH + "/" + "alarm.mp3"])
                        call(["mpg321", "-q", "--stereo", SCRIPT_PATH + "/" + "alarm.mp3"])
                    except OSError:
                        print("Error playing audio! Make sure you have 'mpg321' installed!")
                print("Deleting alarm", alarms[alarms_list[0]], "from", alarms.keys())
                del alarms[alarms_list[0]]
                alarms_list.pop(0)
                print("Deleted", alarms.keys())
            else:
                print("No alarms for another " +
                      str(dt.strptime(alarms_list[0], "%Y-%m-%d-%H:%M:%S") - dt.now()) + "(hh:mm:ss.ms)")
                print("Taking a nap")
                sleep((dt.strptime(alarms_list[0], "%Y-%m-%d-%H:%M:%S") - dt.now()).total_seconds())
            alarms_list = sorted(alarms)
    else:
        print("No alarm is set yet. Exiting Program!")
    alarms.close()


def set_alarm(time, msg=None, speak=False):
    print("Got args as", time, msg, speak)
    time = str(time).replace(" ","-")
    alarms[time] = msg
    if speak and msg:
        try:
            from gtts import gTTS
            v_msg = gTTS(msg)
            v_msg.save(SCRIPT_PATH + "/" + time + ".mp3")
        except ImportError:
            print("There won't be any speech output! gTTS is not installed! Default Alarm tone will be played!")
            call(["cp",
                  SCRIPT_PATH + "/" + "alarm.mp3",
                  SCRIPT_PATH + "/" + time + ".mp3"]
                 )
            pass
    run()

try:
    parser = argparse.ArgumentParser(description="Simple Alarm/ToDo/Reminder App using native notify-send library and" +
                                                 " python libraries!")
    parser.add_argument("time", type=str, help="Enter time in hh:mm (24hrs format)")
    parser.add_argument("-m", type=str,
                        help="Enter you message enclosed in quotes eg. \"Hello world\"",
                        nargs=1,
                        default=None)
    parser.add_argument("-d",
                        help="Enter date in dd-mm-yyyy format",
                        nargs=1
                        )
    parser.add_argument("-e",
                        help="if you want to delete your alarm/reminder"
                        )
    parser.add_argument("-s",
                        help="if you want your message to be spoken out loud. Make sure you have internet " +
                             "connectivity and have 'gTTS' and mpg321 installed. default ring is played if -m is not" +
                             " set.",
                        action="store_true"
                        )

    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            if sys.argv[1] == '-e':
                alarm_list = alarms.keys()
                if alarm_list:
                    print("Sr. No.\t\tTime\t\tMessage")
                    for i in enumerate(alarm_list):
                        print(i[0], '.\t', i[1], '\t', alarms[i[1]])
                    delete_in = raw_input("Please enter the index you want to delete: ")
                    if delete_in != '':
                        del alarms[alarm_list[int(delete_in)]]
                        if os.path.isfile(SCRIPT_PATH + "/" + alarm_list[int(delete_in)]+".mp3"):
                            os.remove(SCRIPT_PATH + "/" + alarm_list[int(delete_in)]+".mp3")
                else:
                    print("No alarms set yet!")
                sys.exit(0)
        else:
            pass
        args = parser.parse_args()
        print(args)
        if args.d is not None:
            dd, mm, yyyy = [int(i) for i in args.d[0].split("-")]
            input_date = datetime.date(yyyy, mm, dd)
        else:
            input_date = dt.date(dt.now())
        if args.m is not None:
            input_msg = args.m[0]
        else:
            input_msg = None
        input_speak = args.s
        HH, MM = [int(i) for i in args.time.split(":")]
        input_time = dt.combine(input_date, datetime.time(HH, MM))
        if input_time < dt.now():
            input_time += timedelta(days=1)
        print(input_time, input_msg, input_speak)
        set_alarm(input_time, input_msg, input_speak)

    # run alarm func
    else:
        run()

except KeyboardInterrupt:
    print("Forced Closing the application...")
finally:
    print("Closing the file...")
    alarms.close()
    print("Closed @", str(dt.now()))
