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

def main(args):
    if len(args) < 1:
        print "Not enough arguments. Exiting."; return
    content_index = args[0].find("content:")
    arg = args[0]
    r_str = ''
    if not -1 == content_index:
        if not len(args) == 1:
            print "Too many arguments. Exiting."; return
        r_str_init = "http://builder-solr-slave.dev.trove.com:7979/solr/select/?q=" + args[0] + \
                            "&qt=troveapihandler&recency=1&rows=1&fl=channel" 
        r_init = requests.get(r_str_init)
        num_found = r_init.text[r_init.text.find('"numFound":')+12:r_init.text.find('"start":')-1]
        r_str = "http://builder-solr-slave.dev.trove.com:7979/solr/select/?q=" + args[0] + \
                            "&qt=troveapihandler&recency=1&rows=" + num_found + "&fl=channel" 

    else:
        # assume it is an OR, ie a more 'english' query than 'content:65022595004265876'.
        arg = '+'.join(args)
        # arg = re.sub('"', '\"', arg)
        r_str_init = "http://solr.dev.trove.com:7979/solr/select/?q=%28%22" + arg + \
                            "%22%29%0D%0A&version=2.2&start=0&rows=1&indent=on" 
        r_init = requests.get(r_str_init)
        nf = r_init.text[r_init.text.find('numFound')+10:]
        nf = nf[:nf.find(',')] 
        r_str = "http://solr.dev.trove.com:7979/solr/select/?q=%28%22" + arg + \
                "%22%29%0D%0A&version=2.2&start=0&rows=2917&indent=on" 

    
    print "requesting \'%s\'..." % r_str
    r = requests.get(r_str)
    if not r.status_code == 200:
        print "status: ", r.status_code, " <", r.reason, ">. Exiting."; return
    else:
        print "successful request."


#####  find and rank the related channels:
    text_str = r.text
    contbit = True
    startbit = True
    chnls = []
    while contbit:
        rc_id = text_str.find(tag_name)
        if rc_id == -1 or text_str.find('facet_counts') < rc_id: # <- end before facets section
            contbit = False; break;
        text_str = text_str[rc_id+1:]
        if startbit:
            startbit = False
        else:
            related = text_str[len(tag_name)+2:match_parenthesis(text_str)] # somewhat robust
            related = re.sub('\"', '', related)
            rels = related.split(",")
            for r_ch in rels:
                while not r_ch[0].isdigit():
                    r_ch = r_ch[1:]
                chnls.append(r_ch)
            counts = []
    for ch in chnls:
        newl = findsubelem(ch, counts, 0)
        if None == newl:
            counts.append([ch, 1])
        else:
            newl[1] = newl[1]+1;

    counts.sort(key=lambda x: x[1])
    counts.reverse()

    print "All channels directly related to channel \'%s\':" % arg
    for rc in counts:
        print " -> ", rc[0], "(count:", rc[1], ")"

#####  find facets:
    text_str = text_str[text_str.find('"facet_counts":')+16:-1]
    print "Found facets for the query: [todo]"
    facets = []

    while True:
        facet_id = text_str.find('"facet_');
        if facet_id == -1: break;
        else: text_str = text_str[facet_id+1:]
        field_name = text_str[:text_str.find('"')]
        



if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

