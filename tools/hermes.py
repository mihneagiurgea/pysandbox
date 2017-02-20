import urlparse
import requests
from scrapy.selector import Selector

# Where to download .torrent files?
TORRENT_DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads/torrents')

def get_torrent(url):
    response = requests.get(url)
    sel = Selector(text=response.text)
    path = sel.xpath('//div[@class="results"]//dt[1]/a/@href').extract()[0]
    torrent_url = 'https://%s%s' % (urlparse.urlsplit(url).netloc, path)

