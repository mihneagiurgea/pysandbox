import urllib
from pprint import pprint

from BeautifulSoup import BeautifulSoup

URL = 'http://www.rockfm.ro/rhcp/'

def get_html():
    f = urllib.urlopen(URL)
    html = f.read()
    f.close()
    return html

def get_scores():
    html = get_html()
    soup = BeautifulSoup(html)

    scores = {}

    div = soup.find('div', { 'id': 'rhcp-main'})
    ul = div.findChild('ul')
    for li in ul.findChildren('li'):
        name = li.findChildren()[1].text
        percent = li.findChildren()[3].text
        percent = float(percent.rstrip('%'))
        scores[name] = percent

    return scores

if __name__ == '__main__':
    scores = get_scores()
    pprint(scores)
    print 'Total: %.6f%%' % sum(scores.values())