# Scrape Dropbaout.
from datetime import date
import glob
import json
import os
import random
import re
import shutil
import time

from scrapy.selector import Selector
import requests


COOKIES = {
    'sessionid': 'welms0puiogh8bmkcew3xegpi63006wr',
    'csrftoken': 'IMRKJxUXkbuQGmSnjH3ejKLuWlKpkCsV',
}
HEADERS_RAW = """
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:ro,en-US;q=0.8,en;q=0.6
Cache-Control:no-cache
Connection:keep-alive
Host:about.dropboxer.net
Pragma:no-cache
Referer:https://www.dropbox.com/
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36
"""
HEADERS = {}
for line in HEADERS_RAW.split('\n'):
    if line:
        k, v = line.split(':', 1)
        HEADERS[k] = v


class Config(object):

    BASE_URL = 'https://about.dropboxer.net/dropabout/'
    FILTER_URL = 'https://about.dropboxer.net/dropabout/filter?organization='
    DIR = '/Users/skip/Documents/Dropboxers'
    PHOTOS_DIR = '/Users/skip/Documents/Dropboxers/photos'

    def __init__(self, organization=None, expected_min=None):
        if organization is None:
            self.url = Config.BASE_URL
            self.token = ""
            self.min = expected_min or 1500
        else:
            self.url = Config.FILTER_URL + organization
            self.token = "%s-" % organization.lower()
            self.min = expected_min or 100

    def get_glob_pattern(self):
        return '%s/dropboxers-%s2*.txt' % (self.DIR, self.token)

    def get_cache_fname(self):
        return '%s/cache/cache-%s%s.html' % (self.DIR, self.token, self._today())

    def _get_dropboxers_filename(self):
        return '%s/dropboxers-%s%s.json' % (self.DIR, self.token, self._today())

    def load_dropboxers(self):
        filename = self._get_dropboxers_filename()

        # Does the file for today already exist?
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = json.load(f)

            if len(lines) < self.min:
                print 'WARNING - %s only contains %d lines, re-scraping' % \
                    (filename, len(lines))
                return None
            return lines

        return None

    def dump_dropboxers(self, dropboxers):
        fname = self._get_dropboxers_filename()

        with open(fname, 'w') as f:
            json.dump(dropboxers, f, indent=4)

            print 'Wrote %d Dropboxers to %s' % (len(dropboxers), fname)

    def get_events_new_fname(self):
        return '%s/events-%snew.txt' % (self.DIR, self.token)

    def get_events_left_fname(self):
        return '%s/events-%sleft.txt' % (self.DIR, self.token)

    def _today(self):
        return date.today().strftime('%Y-%m-%d')


def download_image(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print 'Downloaded photo to %s' % path
    else:
        print 'Error %s while downloading %s' % (r.status_code, url)


def download_some_images(config, dropboxers, count=25):
    base_dir = config.PHOTOS_DIR
    for dropboxer in dropboxers:
        photo_url = dropboxer['photo']
        filename = photo_url.rsplit('/', 1)[1]
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            continue

        download_image(photo_url, path)
        to_sleep = random.random() * 5
        time.sleep(to_sleep)

        count -= 1
        if count == 0:
            break


JS_VAR_PATTERN = 'var filteredDropboxers = new Dropboxers\((.*?)\);$'


def scrape_all(content):
    lines = content.splitlines()
    for line in lines:
        m = re.search(JS_VAR_PATTERN, line)
        if m is not None:
            break

    assert m is not None, "Pattern %r not found" % JS_VAR_PATTERN

    return json.loads(m.groups(1)[0])


def fetch_cached(config):
    fname = config.get_cache_fname()

    if os.path.exists(fname):
        print 'Reading from %s cache' % fname
        return open(fname).read()

    url = config.url
    r = requests.get(url, headers=HEADERS, cookies=COOKIES)
    if 'Mihnea' not in r.content:
        print 'Error, could not fetch %s:\n%s' % (url, r.content)
        return None

    print 'Read %dB from %s' % (len(r.content), url)
    with open(fname, 'w') as f:
        f.write(r.content)
    print 'Cached into %s' % fname

    return r.content


def scrape(config):
    dropboxers = config.load_dropboxers()
    if dropboxers is not None:
        print 'Already scraped %d droboxers for today.' % len(dropboxers)
        return dropboxers

    content = fetch_cached(config)
    assert content, "fetch_cached returned None"

    dropboxers = scrape_all(content)
    assert len(dropboxers) > 0, "Found no dropboxers, aborting"

    config.dump_dropboxers(dropboxers)
    return dropboxers


def recompute_all_deltas(config):

    def write_events(f, tail, events):
        f.write('\t%s: %d new\n' % (tail, len(events)))
        f.writelines(events.values())
        f.write('\n')

    fnames = glob.glob(config.get_glob_pattern())
    assert fnames == sorted(fnames)

    with open(config.get_events_new_fname(), 'w') as fadds:
        with open(config.get_events_left_fname(), 'w') as frems:

            items_base = read_items(fnames[0])
            for fname in fnames[1:]:
                tail = os.path.split(fname)[1]

                items_new = read_items(fname)
                adds, rems = compute_deltas(items_base, items_new)
                if adds:
                    print 'File %s -> %2d new adds' % (tail, len(adds))
                    write_events(fadds, tail, adds)
                if rems:
                    print 'File %s -> %2d new rems' % (tail, len(rems))
                    write_events(frems, tail, rems)

                items_base = items_new


def read_items(fname):
    items = {}
    with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue

            matches = re.findall('.*\((\S+@)\).*', line)
            assert len(matches) <= 1
            if '(-)' in line:
                # Dropboxer without username, ignore.
                continue
            assert len(matches) == 1, line

            items[matches[0]] = line
    return items


def compute_deltas(items_base, items_new):
    new = set(items_new.keys())
    base = set(items_base.keys())

    adds = {}
    for uname in new - base:
        adds[uname] = items_new[uname]

    rems = {}
    for uname in base - new:
        rems[uname] = items_base[uname]

    return adds, rems


def main():
    ORG_TO_EXPECTED_MIN = {
        "Engineering": 300,
        "Product": 50,
        "Design": 50,
        "People": 75,
    }

    for org, expected_min in ORG_TO_EXPECTED_MIN.iteritems():
        print '\n\tOrganization=%s\n' % org
        config = Config(org, expected_min)
        dropboxers = scrape(config)
        download_some_images(config, dropboxers)
        # recompute_all_deltas(Config("Engineering"))


if __name__ == '__main__':
    main()
