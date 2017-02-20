import os
import random
import subprocess
import re

import requests
from scrapy.selector import Selector

# Where to download .torrent files?
TORRENT_DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads/torrents')
# episodecalendar.com login details
EMAIL = 'skipy3@gmail.com'
PASSWORD = 'easy2pass'


def get_episode_details(title):
    """ Returns a (show, season, episode, format) tuple.

    >>> get_episode_details('American Idol S13E14 HDTV x264-2HD')
    ('American Idol', '13', '14', 'HDTV x264-2HD')
    >>> get_episode_details('Blues America 1of2 Woke Up x264 HDTV-MVGroup')
    >>> get_episode_details('Arrow S02E14 HDTV x264-LOL')
    ('Arrow', '02', '14', 'HDTV x264-LOL')
    """
    m = re.match('(.*) S(\d+)E(\d+) (.*)', title)
    if m:
        return m.groups()
    else:
        return None


class Episode(dict):

    def __init__(self, **kwargs):
        assert kwargs['show']
        kwargs['season'] = int(kwargs.pop('season_number'))
        kwargs['episode'] = int(kwargs.pop('episode_number'))
        dict.__init__(self, **kwargs)

    @property
    def uid(self):
        """Unique identifier of this episode, i.e. 'House S03E14'."""
        return '%(show)s S%(season)sE%(episode)s' % self

    @classmethod
    def from_eztv(cls, eztv_episode):
        """Returns a curated episode in format:
        {
            'episode_number': '12',
            'format': '4x12',
            'name': 'Still',
            'season_number': '4',
            'show': 'The Walking Dead',
            'links': [ url1, url2, ... ]
        }
        """
        details = get_episode_details(eztv_episode['title'])
        if details is None:
            return None
        eztv_episode['show'] = details[0]
        eztv_episode['season_number'] = details[1]
        eztv_episode['episode_number'] = details[2]
        eztv_episode['format'] = details[3]
        # Fix broken links (why are they broken?)
        fix_link = lambda l: 'http:' + l if l.startswith('//') else l
        eztv_episode['links'] = map(fix_link, eztv_episode['links'])

        return Episode(**eztv_episode)


def get_my_shows():
    """Return a list with followed shows (from /my-shows)."""
    s = requests.session()
    login_data = {
        'user[email]': EMAIL,
        'user[password]': PASSWORD
    }
    s.post('http://episodecalendar.com/account/sign_in', data=login_data)

    r = s.get('http://episodecalendar.com/my-shows')

    sel = Selector(text=r.content)
    return sel.xpath('//table[contains(@class, "my_shows")]'
                     '//tr/td[1]//a/text()').extract()


def scrape_eztv(pages=5):
    page_urls = ['http://eztv.it/']
    for i in range(1, pages):
        page_urls.append('http://eztv.it/page_%d' % i)

    eztv_episodes = []
    for page_url in page_urls:
        eztv_episodes.extend(scrape_eztv_page(page_url))

    return eztv_episodes


def scrape_eztv_page(url):
    # What does this do?
    response = requests.get(url)
    sel = Selector(text=response.text)

    episodes = []
    trs = sel.xpath(
        '//table[@class="forum_header_border"][5]//tr[position()>2]')
    added_on = None
    for tr in trs:
        added_on_array = tr.xpath('td[@colspan="5"]/b/text()').extract()
        if added_on_array:
            added_on = added_on_array[0]
        else:
            title = tr.xpath('td[2]/a/text()').extract()[0]
            links = tr.xpath(
                'td[3]/a[contains(@class, "download")]/@href').extract()
            episode = {
                'title': title,
                'links': links,
                'added_on': added_on
            }
            curated_episode = Episode.from_eztv(episode)
            if curated_episode:
                episodes.append(curated_episode)
    return episodes


def download_and_open(url, filename):
    """Download and open a.torrent file from url to local filename."""
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

    # Open .torrent file using OS's default app.
    subprocess.call(["open", filename])


def main():
    if not os.path.exists(TORRENT_DOWNLOAD_FOLDER):
        os.makedirs(TORRENT_DOWNLOAD_FOLDER)

    shows = get_my_shows()
    print('Found %d shows: %s...' % (len(shows), shows[:3]))

    eztv_episodes = scrape_eztv()

    followed_episodes = [ep for ep in eztv_episodes if ep['show'] in shows]
    print('Found %d followed episodes from latest eztv pages' %
          len(followed_episodes))

    for episode in followed_episodes:
        filename = os.path.join(
            TORRENT_DOWNLOAD_FOLDER, '%s.torrent' % episode.uid)
        if not os.path.exists(filename):
            url = random.choice(episode['links'])
            print('Downloading torrent for %s from %s to %s...' %
                  (episode.uid, url, filename))
            download_and_open(url, filename)

if __name__ == '__main__':
    main()
    # import doctest
    # doctest.testmod()
