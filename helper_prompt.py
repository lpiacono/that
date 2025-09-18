from imports import *

def ask(prompt):
    
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])

    while True:
        response = raw_input(prompt).lower()
        if response in yes:
            return True
        elif response in no:
            return False
        else:
            print ""
            sys.stdout.write("!! Please respond with 'yes' or 'no' !! \n")

