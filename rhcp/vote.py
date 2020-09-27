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

def vote():
    email = generate_email()
    print 'Voting as %s' % email
    forgepost(email)

if __name__ == '__main__':
    main()
