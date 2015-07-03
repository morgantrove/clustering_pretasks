# disp_chan_results.py

import sys
import requests 
import string
import re


tag_name = 'channel'


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

# return the sublist in superlist LoLs whose ind'th element is elem
def findsubelem(elem, LoLs, ind):
    if len(LoLs) == 0: return None
    for l in LoLs:
        if elem == l[ind]: 
            return l;
    return None;

def getLabel(ID):
    req_file = requests.get("http://internal-api.trove.com/channels/"+ID).text;
    req_file = req_file[req_file.find("displayName") + 15:]
    return req_file[:req_file.find('"')]


def disp_ch(_id, count):
    print "#" + _id + " (count " + str(count) + ")\t: " + getLabel(_id)

def disp_ch(_id, count, label):
    print "#" + _id + " (count " + str(count) + ")\t: " + label

def disp_ch(_id, count, label, ncount):
    print "#" + _id + " (" + str(count) + "  --  " + str(ncount) + "): " + label

def getFacetChannels(corp):
    chnls = corp[corp.find('"facet_fields":')+1:]
    chnls = chnls[chnls.find('[')+1:]
    chnls = chnls[:chnls.find(']')]
    ch_list = chnls.split(",")

    f_chnls = []
    for i in range(len(ch_list)/2): # mod 2 is given.
        ent_id = ch_list[2*i].strip().strip('"')
        ecount = ch_list[2*i+1].strip()
        # disp_ch(ent_id, ecount) # if desired.
        f_chnls.append([ent_id, int(ecount), getLabel(ent_id)])
    return f_chnls
        


def main(args):
    if len(args) < 1:
        print "Not enough arguments. Exiting."; return
    arg = args[0] # Takes a well-formed, whitespace-free solr query.
    r_str = ''

    # *  Users must ensure they use the _ASCII_ ' \" ', ie backslash & ascii-ambi-quote, in their arguments
    # *  Otherwise, the quotes are not recognized by SOLR.  Example correct expression:
    # *    \"Street+Food\"+OR+\"Food+Trucks\"+OR+\"Artisan+Food+Wagons\"+OR+\"Food+Wagons\"

    r_str = "http://solr.dev.trove.com:7979/solr/select?indent=on&version=2.2&q=%28" + arg + \
            "%29&start=0&rows=1&fl=facets&fq=&hl.fl=&explainOther=&qt=&wt=" 

    
    print " > Requesting \'%s\'..." % r_str
    r = requests.get(r_str)
    if not r.status_code == 200:
        print "status: ", r.status_code, " <", r.reason, ">. Exiting."; return
    print " > Successful request.  Working..."
    f_chnls = getFacetChannels(r.text)
    sumCounts = 0.0 # <- float!
    for ch in f_chnls:
        sumCounts += ch[1]
    for ch in f_chnls:
        ch.append(ch[1] / sumCounts)
        disp_ch(ch[0], ch[1], ch[2], ch[3]) # if desired.


    print " > Processing complete. "

    ###  Channel format:  [string ID number, int count, string english label, float normed count]  ###
    ###  The formatted list of channels is the useful object to be returned or whatnot.

        



if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

