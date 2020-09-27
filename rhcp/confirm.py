import time
import re
import requests
import random

from gmail import read_gmail
from generate import generate_email
from forgepost import forgepost

def main():
    while True:
        vote()
        time.sleep(random.randint(7, 18))
        confirm_emails()
        print 'Sleeping a minute...'
        time.sleep(random.randint(41, 81))

def vote():
    email = generate_email()
    print 'Voting as %s' % email
    forgepost(email)

def confirm_emails():
    for msg in read_gmail():
        if (msg['from'] != 'RockFM <no-reply@rockfm.ro>' or
            msg['subject'] != 'RockFM | Confirma votul tau!'):
            print 'Ignored email from %(from)r subject: %(subject)r' % msg
            continue
        links = get_links(msg)
        if not links:
            print 'No links found for %(subject)s' % msg
        for link in links:
            confirm_link(link)

def get_links(msg):
    text = msg.get_payload()
    return re.findall("<a href='(\S*)'>", text)

def confirm_link(link):
    print 'Confirming %r...' % link
    response = requests.get(link)
    if response.status_code != 200:
        print 'Invalid response %s: %s' % (response.status_code, response.text)

if __name__ == '__main__':
    main()
