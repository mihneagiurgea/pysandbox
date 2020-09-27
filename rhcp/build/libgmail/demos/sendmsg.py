#!/usr/bin/python2.3
#
# sendmsg.py -- Demo to send a message via Gmail using libgmail
#
# $Revision: 1.1 $ ($Date: 2004/07/11 11:42:18 $)
#
# Author: follower@myrealbox.com
#
# License: GPL 2.0
#
import os
import sys
import logging

# Allow us to run using installed `libgmail` or the one in parent directory.
try:
    import libgmail
    logging.warn("Note: Using currently installed `libgmail` version.")
except ImportError:
    # Urghhh...
    sys.path.insert(1,
                    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                  os.path.pardir)))

    import libgmail

    
if __name__ == "__main__":
    import sys
    from getpass import getpass

    try:
        name = sys.argv[1]
        to = sys.argv[2]
        subject = sys.argv[3]
        msg = sys.argv[4]
    except IndexError:
        print "Usage: %s <account> <to address> <subject> <body>" % sys.argv[0]
        raise SystemExit
        
    pw = getpass("Password: ")

    ga = libgmail.GmailAccount(name, pw)

    print "\nPlease wait, logging in..."

    ga.login()

    print "Log in successful.\n"
    gmsg = libgmail.GmailComposedMessage(to, subject, msg)

    if ga.sendMessage(gmsg):
        print "Message sent `%s` successfully." % subject
    else:
        print "Could not send message."

    print "Done."
