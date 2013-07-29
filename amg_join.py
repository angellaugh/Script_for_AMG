# python2.5.1
# author : eric zhang
# email  : ericnomail@gmail.com
# twitter: @loveisbug
#    http://weibo.com/loveisbug
# date        version    PIC    comments
# 20110720    0.0.1      eric   
# 20110725    0.0.2      eric   can use, a bug "ContemporaryR&B;"(first style).
# 20110726    0.1.0      eric   solved ';' issue, solved no style issue.
# 20110804    0.1.1      eric   solved the HTML entity codes conversion issue, use HTMLParser.
# 20110828    0.1.2      eric   split '/' in label and remove space.
# 20111227    0.1.3      eric   support multi '/' in label.
# 20120529    0.2.0      eric   support new version of AMG.
# 20120607    0.2.1      eric   get the 'CD' label.
# 20130305    0.2.2      eric   solved the HTML entity codes conversion issue after update to new version of AMG.
# 20130310    0.2.3      eric   get "GENRE" info while no "STYLES" info. get the label infos of all the album format released.
# 20130311    0.2.4      eric   solved an issue while get album label, only need replace once to get substring.
# 20130312    0.2.5      eric   do not append duplicated label info.

import urllib
import string
import HTMLParser
from BeautifulSoup import BeautifulSoup

def tag_from_amg(url):
    # open and parse the webpage
    html_src = urllib.urlopen(url).read()
    parser = BeautifulSoup(html_src, convertEntities=BeautifulSoup.HTML_ENTITIES)
    h = HTMLParser.HTMLParser()
    star = u"星"
    half = u"半"
    lst = []

    # find rating, release date
    rating_str = parser.find('ul', 'ratings')
    if rating_str != None:
        tmp_rating = int(rating_str.findNext('div')['class'][-1:])
        if tmp_rating == 0 or tmp_rating % 2:
            lst.append(str(tmp_rating / 2 + tmp_rating % 2) + star)
        else:
            lst.append(str(tmp_rating / 2 + tmp_rating % 2) + star + half)
    else:
        lst.append("0" + star)
    rel_date = parser.find('div', 'release-date')
    if rel_date != None:
        lst.append(rel_date.text[-4:])

    # find style tags
    find_result = parser.findAll('div', 'styles')
    if len(find_result) > 0:
        styles = find_result[0].findAll('a')
        for style in styles:
            lst.append(h.unescape(style.text).replace(" ", ""))
    else:
        lst.append(parser.find('div', 'genres').text.replace(" ", ""))

    # find label
    html_src = urllib.urlopen(url + '/releases').read()
    parser = BeautifulSoup(html_src, convertEntities=BeautifulSoup.HTML_ENTITIES)
    find_result = parser.findAll('div', 'label')
    for album in find_result: #if album.text == "CD":
        label_lst = []
        label_ori = h.unescape(album.text).replace(" ", "")
        label_lst.append(label_ori)
        mul_label = label_ori.find('/')
        if mul_label != -1:
            label_lst.append(label_ori.replace("/", " "))
        #label_lst.append(album.findNext('strong').findNext('td').text)
        tmp_str = ' '.join(label_lst)
        if not tmp_str in lst:
            lst.append(tmp_str)
    print ' '.join(lst)

tag_from_amg('http://www.allmusic.com/album/dicks-picks-vol-17-boston-garden-9-25-91-mw0000088337')