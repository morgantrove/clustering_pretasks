# disp_chan_results.py

import sys
import requests 
import string


tag_name = 'relatedChannels'


def match_parenthesis(text):
# Returns the index of the matching parenthesis.
    pass



def main(args):
    if len(args) != 1:
        print "Improper number of arguments. Exiting."; return
    arg = args[0]
    if not arg.isdigit():
        print "Improper argument format: not an integer ID. Exiting."; return

    # Argument 'arg' taken as the channel ID number.

    r_str = "http://internal-api.trove.com/channels/" + arg + "/result"
    print "requesting \'%s\'..." % r_str
    r = requests.get(r_str)
    if not r.status_code == 200:
        print "status: ", r.status_code, " <", r.reason, ">. Exiting."; return
    else:
        print "successful request."
    
    text_str = r.text
    contbit = True
    while contbit:
        rc_id = text_str.find(tag_name)
        if rc_id == -1:
            contbit = False; break;
        text_str = text_str[rc_id+1:]
        related = text_str[:match_parenthesis(text_str)]

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

