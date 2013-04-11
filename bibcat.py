#!/usr/bin/env python

import codecs, unicodedata
import urllib
import feedparser
import io, time, sys, re

def get_as_bibtex (buf):
    return get_as_bibtex_no_regex(buf)


def get_as_bibtex_no_regex (buf):
    """
        Loads a string of lines as a dictionry consisting of relevant bibtex fields.
    """

    result = { 'raw': buf }

    t = 1
    while t < len(buf):
        k = [c.strip() for c in buf[t].split('=', 1)]
        
        if len(k) == 1:
            t = t + 1
            continue

        content = k[1].strip()

        while not (content.endswith('},') or content.endswith('}')):
            t = t + 1
            content = content + ' ' + buf[t].strip()

        key = k[0].strip('{},')
        content = content.strip('{},')

        result[key] = content

        t = t + 1
    
    return result
    

def parse_listings (lines):
    """
        Reads an entire bibtex file and returns a list of bibtex dictionaies.
    """

    listings = []

    collect = False
    inside_comment = False

    buf = []

    for line in lines:
        line = line.strip()
        if line.startswith("@comment"):
            if line.endswith("]"):
                continue

            inside_comment = True

        if line.startswith("%"):
            # Skip
            continue

        if line.startswith("@"):
            collect = True

        if collect:
            buf.append(line + '\n')

            if line == "}":
                collect = False

                if inside_comment:
                    inside_comment = False
                    buf = []
                    continue

                listings.append( get_as_bibtex(buf) )

                buf = []
        # collect

    return listings


def find_arxiv_category (title, author): # {{{

    # print 'Looking for', title
    #
    clean_title  = urllib.quote(unicodedata.normalize('NFKD', title).encode('ascii', 'ignore'))
    clean_author = urllib.quote(unicodedata.normalize('NFKD', title).encode('ascii', 'ignore'))

    if author:
        url = 'http://export.arxiv.org/api/query?search_query=ti:%(title)s%%20AND%%20au:%(author)s&start=0&max_results=1' % \
                { 'title': clean_title, 'author': clean_author }
    else:
        url = 'http://export.arxiv.org/api/query?search_query=ti:%(title)s&start=0&max_results=1' % \
                { 'title': clean_title }

    # print url
    d = feedparser.parse(url)

    try:
        found_title = d['entries'][0]['title'].replace('\n', '').replace('\r', '').replace('\t', ' ')
    except:

        # If we passed in an author, trying searching without that.

        if author:
            return find_arxiv_category(title, author=None)

        # print "Cant find:", title, author
        return None

    category = ''

    try:
        category = d['entries'][0]['arxiv_primary_category']['term']
    except:
        pass

    s1 = found_title.lower().replace(' ', '')
    s2 = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').lower().replace(' ', '')

    dist = distance(s1, s2)
    
    meanlen = (len(s1) + len(s2)) / 2.

    # We look for trivial differences; but we note also that this is only about
    # finding the main group for this paper; and so an exact matching is not
    # necessary.
    
    ratio = 0

    if dist > 0:
        ratio = meanlen / float(dist)
    
    if dist <= 10 and ratio < .5 and category:
        return category
    else:
        pass
    
    return None
# }}}


# From
# http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/
def dameraulevenshtein (seq1, seq2): # {{{
    """Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    >>> dameraulevenshtein('ba', 'abc')
    2
    >>> dameraulevenshtein('fee', 'deed')
    2

    It works with arbitrary sequences too:
    >>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
    2
    """
    # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)

            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)

    return thisrow[len(seq2) - 1]
# }}}

distance = dameraulevenshtein


if __name__ == "__main__": # {{{

    if len(sys.argv) <= 1:
        print 'Please provide at bibfile.'
        exit(1)

    bibfile = sys.argv[1]

    if not bibfile:
        print 'Please provide a bibfile.'
        exit(1)

    f = codecs.open(bibfile, "r", "utf-8")
 
    print 'Reading ...'
    lines = f.readlines()

    print 'Parsing ...'
    listings = parse_listings(lines)

    cats = {"nocat": []}

    print 'Querying ...'

    start = 0
    to = len(listings)

    for k in range(start, to):
        authors = listings[k]['author']
        author = authors.split(' and ')[0]

        cat = find_arxiv_category(listings[k]['title'], author)
        time.sleep(3)

        if cat:
            clean_title = unicodedata.normalize('NFKD', listings[k]['title']).encode('ascii', 'ignore')
            print 'Found: %s' % (clean_title,)

            if cat not in cats:
                cats[cat] = [ listings[k] ]
            else:
                cats[cat].append( listings[k] ) 
        else:
            cats["nocat"].append( listings[k] )

    for k, v in cats.items():
        if len(v) >= 1:
            with open(k + ".bib", "w") as f:
                for bib in v:
                    f.writelines(bib['raw'])
# }}}
