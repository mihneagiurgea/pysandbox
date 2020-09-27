#!/usr/bin/python2.3
#
# archive.py -- Demo to archive all threads in a Gmail folder
#
# $Revision: 1.6 $ ($Date: 2004/07/10 23:06:49 $)
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
    except IndexError:
        name = raw_input("Gmail account name: ")
        
    pw = getpass("Password: ")

    ga = libgmail.GmailAccount(name, pw)

    print "\nPlease wait, logging in..."

    ga.login()

    print "Log in successful.\n"

    searches = libgmail.STANDARD_FOLDERS + ga.getLabelNames()

    while 1:
        try:
            print "Select folder or label to archive: (Ctrl-C to exit)"
            print "Note: *All* pages of results will be archived."

            for optionId, optionName in enumerate(searches):
                print "  %d. %s" % (optionId, optionName)

            name = searches[int(raw_input("Choice: "))]

            if name in libgmail.STANDARD_FOLDERS:
                result = ga.getMessagesByFolder(name, True)
            else:
                result = ga.getMessagesByLabel(name, True)

            print
            mbox = []
            if len(result):
                for thread in result:
                    print
                    print thread.id, len(thread), thread.subject

                    for msg in thread:
                        print "  ", msg.id, msg.number, msg.subject
                        source = msg.source.replace("\r","").lstrip()
                        mbox.append("From - Thu Jan 22 22:03:29 1998\n")
                        mbox.append(source)
                        mbox.append("\n\n") #TODO:Check if we need either/both?
                import time 
                open("archive-%s-%s.mbox" % (name, time.time()),
                     "w").writelines(mbox)
            else:
                print "No threads found in `%s`." % name
            print
                
        except KeyboardInterrupt:
            print "\n\nDone."
            break
    
