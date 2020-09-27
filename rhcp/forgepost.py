"""
===Request headers===
Accept:application/json, text/javascript, */*; q=0.01
Accept-Charset:ISO-8859-1,utf-8;q=0.7,*;q=0.3
Accept-Encoding:gzip,deflate,sdch
Accept-Language:en-US,en;q=0.8
Cache-Control:no-cache
Connection:keep-alive
Content-Length:110
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Cookie:PHPSESSID=c0adtt1ut399ar0v4v9ge9ddi4; POPUPCHECK=1344972746586; __utma=35016354.1923911296.1344886346.1344886346.1344891127.2; __utmb=35016354.1.10.1344891127; __utmc=35016354; __utmz=35016354.1344886346.1.1.utmcsr=facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/
Host:www.rockfm.ro
Origin:http://www.rockfm.ro
Pragma:no-cache
Referer:http://www.rockfm.ro/rhcp/
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1
X-Requested-With:XMLHttpRequest

"""

import requests
import simplejson as json
from pprint import pprint

POST_URL = 'http://www.viralsweep.com/ajax/entry.php'

# TODO(s)
# forge name to look like mine, but slightly different
# forge address to an inexistent unit # (1831)
# http://virl.io/oPoGtOGO
# http://virl.io/oPoGtOGO
# http://virl.io/oPoGtOGO
def forgepost():
    headers = {
        'Referer': 'http://www.viralsweep.com/contest/f32fdc3c-30509&framed=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20120405 Firefox/14.0a1',
    }
    # Build form data
    data = {
        'email2': None,
        'email': 's.k.asdfa@gmail.com',
        'id': 'f32fdc3c-30509',
        'extra': '&first-name=Mihnea&last-name=Giurgea&address=55 9tdh St. #1605&city=San Fsrancisco&state=Califoxrnia&country=United bStates&zip=94103',
        'newsletter': 'no',
        'slid': 77816417, # 77940401
    }
    response = requests.post(POST_URL, data=data, headers=headers)
    if response.status_code != 200:
        raise ValueError('Invalid response: %r' % response)
    text = response.text
    print "Got respnse len=%d:\n%s\n" % (len(text), text)
    # data = json.loads(text)
    # if data.get('trupe'):
    #     votes = {}
    #     for trupa in data.pop('trupe'):
    #         votes[trupa[u'trp_nume']] = int(trupa[u'trp_voturi'])
    #     total = sum(votes.values())
    #     results = votes.items()
    #     results.sort(key=lambda i: i[1], reverse=True)
    #     results = results[:5]
    #     print '     Top %d bands:' % len(results)
    #     for index, (band, v) in enumerate(results):
    #         print '%d) %13s: %5d/%d votes (%.2f%%)' % \
    #               (index + 1, band, v, total, 100.0 * v / total)
    # pprint(data)

if __name__ == '__main__':
    forgepost()
