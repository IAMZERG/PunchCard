#!/usr/bin/python3


#note: os.path.dirname(os.path.realpath(__file__)) = this file's path on the computer
import time
import pickle
import argparse
import os

# # class FooAction(argparse.Action):
    # # def __call__(self, parser, namespace, values, option_string=None):
       # # print('Hello, world!')
       # # setattr(namespace, self.dest, values)
# # class BarAction(argparse.Action):
    # # def __call__(self, parser, namespace, values, option_string=None):
       # # print('%r %r %r' % (namespace, values, option_string))
       # # setattr(namespace, self.dest, values)

class PunchInOut(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open(os.path.dirname(os.path.realpath(__file__))+"/current_timesheet.txt", mode="rb") as current_timesheet:
            sheet_name=pickle.load(current_timesheet)
            with open(os.path.dirname(os.path.realpath(__file__))+"/pickle_"+sheet_name, mode="rb") as picklefile:
                print(os.path.dirname(os.path.realpath(__file__))+"/pickle_"+sheet_name)
                try:
                    timedict = pickle.load(picklefile)
                    timedict["punch_times"].append(time.time())
                    curr_time = time.ctime(timedict["punch_times"][-1])
                    #if you're already punched in, this happens:
                    if (timedict["punched_in"][len(timedict["punched_in"])-1]):
                        print("Successfully punched out at: " + curr_time)
                        desc = input("Description:  ")
                        timedict["desc"].append(desc)
                        timedict["punched_in"].append(False)
                    #if you aren't already punched in, this happens:
                    else:
                        print("Successfully punched in at: " + curr_time)
                        desc = input("Description:  ")
                        timedict["desc"].append(desc)
                        timedict["punched_in"].append(True)
                except EOFError:
                    timedict = {"punched_in": [True], "desc": ["first punch"],"punch_times":[time.time()]}

            with open(os.path.dirname(os.path.realpath(__file__))+"/pickle_"+sheet_name, mode="wb") as picklefile:
                    pickle.dump(timedict, picklefile)

class TimesheetPrint(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open(os.path.dirname(os.path.realpath(__file__))+"/current_timesheet.txt", mode="rb") as current_timesheet:
            
            sheet_name=pickle.load(current_timesheet)
            with open(os.path.dirname(os.path.realpath(__file__))+"/timesheet_"+sheet_name, "w") as timecard:
                with open(os.path.dirname(os.path.realpath(__file__))+"/pickle_"+sheet_name, "rb") as picklefile:
                    try:
                            timedict = pickle.load(picklefile)
                    except IOError:
                            print("There was an error in loading timestamps")
                            pass
                my_dict = zip(timedict["punch_times"], timedict["desc"], timedict["punched_in"])
                for (punch, desc, punched_in) in my_dict:
                        if (punched_in):
                                status="in"
                        if (not punched_in):
                                status="out"
                        timecard.write("Punched " + status + " at " + time.ctime(punch) + "  Description:  " + desc + "\n")
                #calculating the total time:
                if (timedict["punched_in"][-1]):
                        total_time=0
                        for index, punch in enumerate(timedict["punch_times"][:-1:2]):  #using the [start:stop:step] notation to my advantage
                                total_time = punch - timedict["punch_times"][index+1]
                else:
                        for index, punch in enumerate(timedict["punch_times"][::2]):
                                total_time = punch - timedict["punch_times"][index+1]
                timecard.write("\tTotal time:  " + str(total_time/60/60) + " hours.")
                print("Timesheet created successfully.  Filename: ", "timesheet_"+sheet_name)

#current_timesheet will be the current active timesheet.
class NewTimesheet(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        filename=input("Enter a file name for the new timesheet.  Include a file extension (preferably .txt)?\n")
        with open(os.path.dirname(os.path.realpath(__file__))+"/current_timesheet.txt", mode="wb+") as current_timesheet:
            pickle.dump(filename, current_timesheet)
            
                
	   
# def punch_in_or_out ():
    # with open("timedict.txt", "rb") as picklefile:
        # try:
            # timedict = pickle.load(picklefile)
        # except:
            # timedict = {"punched_in": [True],
                        # "desc": ["first punch"],
                        # "punch_times":[time.time()]}
    # timedict["punch_times"].append(time.time())
    # curr_time = time.ctime(timedict["punch_times"][-1])
    # #if you're already punched in, this happens:
    # if (timedict["punched_in"][-1]):
        # print("Successfully punched out at: " + curr_time)
        # desc = input("Description:  ")
        # timedict["desc"].append(desc)
        # timedict["punched_in"].append(False)
    # #if you aren't already punched in, this happens:
    # else:
        # print("Successfully punched in at: " + curr_time)
        # desc = input("Description:  ")
        # timedict["desc"].append(desc)
        # timedict["punched_in"].append(True)
    # with open("timedict.txt", "wb") as picklefile:
        # pickle.dump(timedict, picklefile)

# def timesheet ():
    # with open("test_timecard.txt", "w") as timecard:
        # with open("timedict.txt", "rb") as picklefile:
            # try:
                # timedict = pickle.load(picklefile)
            # except:
                # print("There was an error in loading timestamps")
        # my_dict = zip(timedict["punch_times"], timedict["desc"], timedict["punched_in"])
        # for (punch, desc, punched_in) in my_dict:
            # if (punched_in):
                # status="in"
            # if (not punched_in):
                # status="out"
            # timecard.write("Punched " + status + " at " + time.ctime(punch) + "  Description:  " + desc + "\n")
        # #calculating the total time:
        # if (timedict["punched_in"][-1]):
            # total_time=0
            # for index, punch in enumerate(timedict["punch_times"][:-1:2]):  #using the [start:stop:step] notation to my advantage
                # total_time = punch - timedict["punch_times"][index+1]
        # else:
            # for index, punch in enumerate(timedict["punch_times"][::2]):
                # total_time = punch - timedict["punch_times"][index+1]
        # timecard.write("\tTotal time:  " + str(total_time/60/60) + " hours.")

###############################################
          #OPTION HANDLING
###############################################


parser = argparse.ArgumentParser()
parser.add_argument('--in', '--out', '-i', '-o', nargs=0, action=PunchInOut, help='Creating a punch in entry.  Prompts for a description')
parser.add_argument('--timesheet', '-t', nargs=0, action=TimesheetPrint, help='Creating a timesheet from the punches in the punch list.')
parser.add_argument('--new', '-n', nargs=0, action=NewTimesheet, help='Making new timesheet, punching into it.')
# parser.add_argument('--change', '-c', action=Change, help='Change to a different timesheet, punch into it.')
parser.parse_args()
