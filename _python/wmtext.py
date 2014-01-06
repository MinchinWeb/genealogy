'''WMText
v.2 - WM - Jan. 5, 2014

This is a helper file, containing formatting helps for creating command line
programs.
'''

version = 2

import colorama
import sys
import time

def centered (mystring, linewidth=79, fill=" "):
	'''Takes a string, centers it, and pads it on both sides'''
	sides = (linewidth - len(mystring))/2
	sidestring = ""
	for i in range(sides):
		sidestring = sidestring + fill
	newstring = sidestring + mystring + sidestring
	while len(newstring) < linewidth:
		newstring = newstring + " "
	return newstring

def clock_on_right(mystring):
	'''Takes a string, and prints it with the clock right aligned'''
	taken = len(mystring)
	padding = 79 - taken - 5
	clock = time.strftime("%I:%M", time.localtime())
	print mystring + " "*padding + clock
	
def query_yes_no(question, default="yes"):
    '''Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    
	Copied from
	http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
	'''
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
							 
def query_yes_no_all(question, default="yes"):
    '''Ask a yes/no/all question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no", "all" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes", "no", or "all".
	'''
    valid = {"yes":1,  "y":1,  "ye":1,
             "no":0,   "n":0,
			 "all":2,  "a":2,  "al":2}
    if default == None:
        prompt = " [y/n/a] "
    elif default == "yes":
        prompt = " [Y/n/a] "
    elif default == "no":
        prompt = " [y/N/a] "
    elif default == "all":
        prompt = " [y/n/A] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes', 'no', or 'all' "\
                             "(or 'y', 'n' or 'a').\n")

def query_yes_quit(question, default="quit"):
    '''Ask a yes/quit question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "quit" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "quit".
    
	Modified from
	http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
	'''
    valid = {"yes":True,   "y":True,  "ye":True,
             "quit":False,     "q":False}
    if default == None:
        prompt = " [y/q] "
    elif default == "yes":
        prompt = " [Y/q] "
    elif default == "quit":
        prompt = " [y/Q] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'quit' "\
                             "(or 'y' or 'q').\n")

def wait(sec):
	'''
	Prints a timer with the format 0:00 to the console,
	and then clears the line when the timer is done
	'''
	while sec > 0:
		sys.stdout.write('\r' + str(sec//60).zfill(1) + ":" + str(sec%60).zfill(2) + '     ')
		sec -= 1
		sleep(1)
		sys.stdout.write('\r' + '           ' + '\r')
		
def title(mytitle):
	print colorama.Style.BRIGHT + colorama.Fore.YELLOW + colorama.Back.BLUE + centered(mytitle) + colorama.Style.RESET_ALL
	
def subtitle(mysubtitle):
	print colorama.Style.BRIGHT + centered(mysubtitle) + colorama.Style.RESET_ALL