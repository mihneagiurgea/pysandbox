import random
import re

def generate_email(email='victor.ponta.paste@gmail.com'):
    username, service = email.split('@')
    N = len(username) - 1
    x = random.randint(1, 2 ** N)
    result = ''
    for i in xrange(0, N):
        result += username[i]
        if x & (1 << i):
            result += '.'
    result += username[N]
    fake_email = '%s@%s' % (result, service)
    # Remove multiple docs
    fake_email = re.sub('\.+', '.', fake_email)
    return fake_email

if __name__ == '__main__':
    for i in xrange(50):
        print generate_email()


