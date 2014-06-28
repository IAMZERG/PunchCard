#!/bin/bash

import time
import sys
import pickle



##this is a terminal-based punchcard program designed for freelancers and contract workers.
##it's dummy software and doesn't do much in the way of error checking or making sure you punch out


##TO MAKE A NEW PUNCHCARD:
##    punch new [PUNCHCARD_NAME] [optional: DESCRIPTION]
##
## NOTE: DESCRIPTION is a description of the project

##PUNCH INTO/OUT OF CURRENT PUNCHCARD:
##    punch (in/out) [PUNCHCARD_NAME]

##TO CREATE A TIMESHEET FOR THE CURRENT PROJECT:
##    punch timesheet [PUNCHCARD_NAME] [FILE_NAME] [optional:HOURLY_RATE] [optional: clear]
##
## NOTE: This timesheet will create a text file with the name "[FILE_NAME].txt"
## NOTE: Adding [HOURLY_RATE] will multiply the billable hours by your hourly rate and give a total due
## NOTE: clear will clear the data from the punchcard--useful if you want to bill someone multiple
##   times over the course of a big project.  Just be sure to use that file before you perform
##   another clear or your data may be lost!!!



##def handle_args():
##    ##this will handle all the function calls and set things up for the rest of the script
##
##    current_time=time.time()
##    arguments=sys.argv()+current_time
##    
##    if (arguments[1]=="new"):
##        new_punchcard(arguments)
##    if (arguments[1]=="in"):
##        punch_in(arguments)
##    if (arguments[1]=="out"):
##        punch_out(arguments)
##    if (arguments[1]=="change"):
##        change_punchcard(arguments)
##    if (arguments[1]=="timesheet"):
##        create_timesheet(arguments)

    
##TO DO: GET NEW_PUNCHCARD FUNCTION WORKING, THEN FORMAT OTHER FUNCTIONS AROUND IT.
    
        
def new_punchcard (arguments):
    
    ##this will create a new punchcard and punch into it
    name=arguments[2]
    punch_time=time.ctime(int(arguments[3]))
    with open(name+"_punchcard.txt", "a+") as card:
        try:
            card.write(punch_time + "\n")
        except (err):
            print("There was an error: "+str(err))
    if (isinstance(arguments[3], float)):    
        punch_var=[arguments[3]]
    else:
        pass
    with open(name+"_punch.pnc", "wb"):
        #do nothing--want to make sure file exists
        pickle.dump(punch_var, name+"_punch.pnc")
    
    
def punch_in (arguments):

    ##This function will punch into a project
    if (isinstance(arguments[3], float)):    
        punch_var=[arguments[3]]
    else:
        print("Error with command.  Try again.")
        pass
    name=arguments[2]
    punch_time=time.ctime(arguments[3])
    with open(name+"_punchcard.txt", "a") as card:
        card.write(punch_time + "\n")
    with open(name+"_punch.pnc", "a+"):
        #do nothing--want to make sure file exists
        pass
    pickle.dump(punch_var, name+"_punch.pnc")


def punch_out (arguments):
        
    ##This will punch out of the current active project
    if (isinstance(arguments[3], float)):    
        punch_var.append(arguments[3])
    else:
        print("Error with command.  Try again.")
        pass
    name=arguments[2]
    punch_time=time.ctime(arguments[3])
    punch_var=pickle.load(name+"_punch.pnc")
    with open(name+"_punchcard.txt", "a") as card:
        card.write(punch_time + "\n\n")
    if (isinstance(arguments[3], float)):    
        punch_var.append(arguments[3])
    else:
        print("Error with command.  Try again.")
        pass
    with open(name+"_punch.pnc", "a"):
        #do nothing--want to make sure file exists
        pass
    pickle.dump(punch_var, name+"_punch.pnc")


def create_timesheet (arguments):
    ##This will create a timesheet text file
    pass



##THIS IS TEST CODE

arguments=input("Enter a command.")
current_time=time.time()
arguments=arguments.split()
arguments.append(current_time)



if (arguments[1]=="new"):
    new_punchcard(arguments)
if (arguments[1]=="in"):
    punch_in(arguments)
if (arguments[1]=="out"):
    punch_out(arguments)
if (arguments[1]=="change"):
    change_punchcard(arguments)
if (arguments[1]=="timesheet"):
    create_timesheet(arguments)


    
