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
    rating_str = parser.find('span', 'hidden')
    if rating_str != None:
        rating = float(rating_str.text)
        if rating * 2 % 2:
            lst.append(str(string.atoi(rating_str.text[:1])) + star + half)
        else:
            lst.append(str(string.atoi(rating_str.text)) + star)
    else:
        lst.append("0" + star)
    rel_date = parser.find('dd', 'release-date')
    if rel_date != None:
        lst.append(rel_date.text[-4:])

    # find style tags
    find_result = parser.findAll('dd', 'styles')
    if len(find_result) > 0:
        styles = find_result[0].findAll('li')
        for style in styles:
            tmp_str = h.unescape(style.text)
            lst.append(tmp_str.replace(" ", ""))
    else:
        lst.append(parser.find('dd', 'genres').text.replace(" ", ""))

    # find label
    html_src = urllib.urlopen(url + '/releases').read()
    parser = BeautifulSoup(html_src, convertEntities=BeautifulSoup.HTML_ENTITIES)
    find_result = parser.findAll('td', 'format')
    for album in find_result: #if album.text == "CD":
        tmp = album.findNext('td').text
        label_ori = h.unescape(tmp.replace(album.findNext('strong').text, ""))
        label = label_ori.replace(" ", "")
        lst.append(label)
        mul_label = label_ori.find('/')
        if mul_label != -1:
            label_div = label.replace("/", " ")
            lst.append(label_div)
        lst.append(album.findNext('strong').findNext('td').text)
    print ' '.join(lst)

tag_from_amg('http://www.allmusic.com/album/strength-in-numbers-mw0000192172')