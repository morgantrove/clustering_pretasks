# disp_chan_results.py

import sys
import requests 
import string
import re


tag_name = 'relatedChannels'


def match_parenthesis(text):
# Returns the index of the matching parenthesis. Returns -1 if unmatched.
    begun = False
    counter = 0
    for c in range(len(text)):
        if counter < 0: return -1
        if text[c] == ('[' or '{' or '('):
            if not begun: begun = True
            counter += 1
        if text[c] == (']' or '}' or ')'):
            counter -= 1
        if counter == 0 and begun: return c
    return -1


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
        related = text_str[len(tag_name)+3:match_parenthesis(text_str)+1]
        rels_list = related[0:match_parenthesis(related)]
        print len(rels_list)
        print ""

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

