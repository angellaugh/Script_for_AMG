# python2.5.1
# author : eric zhang
# email  : ericnomail@gmail.com
# twitter: @loveisbug
#    http://weibo.com/loveisbug
# date        version    PIC    comments
# 20110826    0.0.1      eric   first version.
# 20111011    0.1.0      eric   support multi discs.
# 20130220    0.2.0      eric   not work for xiami, update for allmusic.
# 20130729    0.3.0      eric   patch for AMG upgrading, need to use Rovi API ASAP.

import urllib
import string
from BeautifulSoup import BeautifulSoup

def get_tracks(url):
    parser = BeautifulSoup(urllib.urlopen(url).read())

    discs = parser.findAll('div', 'disc')
    if discs != None:
        i = 1
        for disc in discs:
            print "disc " + str(i)
            i += 1
            tracks = disc.findAll('td', 'tracknum')
            for track in tracks:
                print track.text + ". " + track.findNext('div', 'title').text
            print
    else:
        print "No track list."

get_tracks('http://www.allmusic.com/album/blow-by-blow-wired-mw0001061008')
