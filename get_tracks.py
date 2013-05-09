# python2.5.1
# author : eric zhang
# email  : ericnomail@gmail.com
# twitter: @loveisbug
#    http://weibo.com/loveisbug
# date        version    PIC    comments
# 20110826    0.0.1      eric   first version.
# 20111011    0.1.0      eric   support multi discs.
# 20130220    0.2.0      eric   not work for xiami, update for allmusic.

import urllib
import string
from BeautifulSoup import BeautifulSoup

def get_tracks(url):
    parser = BeautifulSoup(urllib.urlopen(url).read())

    i = 1
    discs = parser.find('div', {'id' : 'tracks'})
    if discs != None:
        disc_table = discs.findAll('div', 'table-container')
        if len(disc_table) > 0:
            i = 1
            for disc in disc_table:
                print "disc " + str(i)
                i += 1
                tracks = disc.findAll('a', 'primary_link')
                j = 1
                for track in tracks:
                    print str(j) + ". " + track.text
                    j += 1
                print
    else:
        print "No track list."

get_tracks('http://www.allmusic.com/album/rhymes-reasons-mw0000207709')
