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
    for c in range(0, len(text)):
        if counter < 0: return -1
        if text[c] == ('[' or '{' or '('):
            counter += 1
            if not begun: begun = True
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
    rels_list = []
    while contbit:
        rc_id = text_str.find(tag_name)
        if rc_id == -1:
            contbit = False; break;
        text_str = text_str[rc_id+1:]
        related = text_str[len(tag_name)+3:match_parenthesis(text_str)] # somewhat robust
        while True:
            relChInx = related.find('}') # _NOT_ robust, on a '}' char in the text body
            if relChInx == -1: break
            relChn = related[0:relChInx].lstrip(", {")
            related = related[relChInx+1:]
            relChn = re.sub('\"', '', relChn[16:-25])
            relChn = re.sub(', id:', ' -- channel ID', relChn)
            if not relChn in rels_list[0]:
                rels_list.append([relChn 0])
        

    print "All channels directly related to channel \'%s\':" % arg
    for rc in rels_list:
        print " -> ", rc, rels_list.count(rc)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

