#!/usr/bin/python2.3
#
# libgmail -- Gmail access via Python
#
# Version: 0.0.5 (11 July 2004)
#
# Author: follower@myrealbox.com
#
# License: GPL 2.0
#
# Thanks:
#   * Live HTTP Headers <http://livehttpheaders.mozdev.org/>
#   * Gmail <http://gmail.google.com/>
#   * Google Blogoscoped <http://blog.outer-court.com/>
#   * ClientCookie <http://wwwsearch.sourceforge.net/ClientCookie/>
#     (There when I needed it...)
#   * The *first* big G. :-)
#
# NOTE:
#   You should ensure you are permitted to use this script before using it
#   to access Google's Gmail servers.
#
#
# Gmail Implementation Notes
# ==========================
#
# * Folders contain message threads, not individual messages. At present I
#   do not know any way to list all messages without processing thread list.
#

from constants import *

import re
import urllib
import urllib2
import logging

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

URL_LOGIN = "https://www.google.com/accounts/ServiceLoginBoxAuth"
URL_GMAIL = "https://gmail.google.com/gmail"

# TODO: Get these on the fly?
STANDARD_FOLDERS = [U_INBOX_SEARCH, U_STARRED_SEARCH,
                    U_ALL_SEARCH, U_DRAFTS_SEARCH,
                    U_SENT_SEARCH, U_SPAM_SEARCH]

versionWarned = False # If the Javascript version is different have we
                      # warned about it?

RE_COOKIE_VAL = 'cookieVal=\W*"(.+)"'
def _extractGV(pageData):
    """

    var cookieVal= "xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

    `pageData` -- HTML page with Javascript to set cookie value.
    """
    gv = None
    
    try:
        gv = re.search(RE_COOKIE_VAL, pageData).group(1)
    except AttributeError:
        print "Error: Couldn't extract GV cookie."
        raise SystemExit

    return gv



RE_SPLIT_PAGE_CONTENT = re.compile("D\((.*?)\);", re.DOTALL)
def _parsePage(pageContent):
    """
    Parse the supplied HTML page and extract useful information from
    the embedded Javascript.
    
    """
    # Note: We use the easiest thing that works here and no longer
    #       extract the Javascript code we want from the page first.
    items = (re.findall(RE_SPLIT_PAGE_CONTENT, pageContent)) 

    # TODO: Check we find something?
    
    itemsDict = {}

    namesFoundTwice = []

    for item in items:
        item = item.strip()[1:-1]
        name, value = (item.split(",", 1) + [""])[:2]

        name = name[1:-1] # Strip leading and trailing single or double quotes.
        
        try:
            # By happy coincidence Gmail's data is stored in a form
            # we can turn into Python data types by simply evaluating it.
            # TODO: Parse this better/safer?
            # TODO: Handle "mb" mail bodies better as they can be anything.
            if value != "": # Empty strings aren't parsed successfully.
                parsedValue = eval(value.replace("\n",""))
            else:
                parsedValue = value
        except SyntaxError:
            logging.warning("Could not parse item `%s` as it was `%s`." %
                            (name, value))
        else:
            if itemsDict.has_key(name):
                # This handles the case where a name key is used more than
                # once (e.g. mail items, mail body) and automatically
                # places the values into list.
                # TODO: Check this actually works properly, it's early... :-)
                if (name in namesFoundTwice):
                    itemsDict[name].append(parsedValue)
                else:
                    itemsDict[name] = [itemsDict[name], parsedValue]
                    namesFoundTwice.append(name)
            else:
                itemsDict[name] = parsedValue

    global versionWarned
    if itemsDict[D_VERSION] != js_version and not versionWarned:
        logging.warning("Live Javascript and constants file versions differ.")
        versionWarned = True

    return itemsDict



class CookieJar:
    """
    A rough cookie handler, intended to only refer to one domain.

    Does no expiry or anything like that.

    (The only reason this is here is so I don't have to require
    the `ClientCookie` package.)
    
    """

    def __init__(self):
        """
        """
        self._cookies = {}


    def extractCookies(self, response, nameFilter = None):
        """
        """
        # TODO: Do this all more nicely?
        for cookie in response.headers.getheaders('Set-Cookie'):
            name, value = (cookie.split("=", 1) + [""])[:2]
            if not nameFilter or name in nameFilter:
                self._cookies[name] = value.split(";")[0]


    def addCookie(self, name, value):
        """
        """
        self._cookies[name] = value


    def setCookies(self, request):
        """
        """
        request.add_header('Cookie',
                           ";".join(["%s=%s" % (k,v)
                                     for k,v in self._cookies.items()]))

        
    
def _buildURL(**kwargs):
    """
    """
    return "%s?%s" % (URL_GMAIL, urllib.urlencode(kwargs))



def _paramsToMime(params):
    """
    """
    mimeMsg = MIMEMultipart("form-data")

    for name, value in params.iteritems():
        mimeItem = MIMEText(value)
        mimeItem.add_header("Content-Disposition", "form-data", name=name)

        del mimeItem['Content-Type']
        del mimeItem['MIME-Version']
        del mimeItem['Content-Transfer-Encoding']

        mimeMsg.attach(mimeItem)

    del mimeMsg['MIME-Version']

    return mimeMsg

    

class GmailAccount:
    """
    """

    def __init__(self, name, pw):
        """
        """
        self.name = name
        self._pw = pw

        self._cachedQuotaInfo = None
        self._cachedLabelNames = None
        
        self._cookieJar = CookieJar()


    def login(self):
        """
        """
        data = urllib.urlencode({'continue': URL_GMAIL,
                                 'service': 'mail',
                                 'Email': self.name,
                                 'Passwd': self._pw,
                                 'null': 'Sign+in'})
    
        headers = {'Host': 'www.google.com',
                   'User-Agent': 'User-Agent: Mozilla/5.0 (compatible;)'}

        req = urllib2.Request(URL_LOGIN, data=data, headers=headers)
        resp = urllib2.urlopen(req)

        self._cookieJar.extractCookies(resp, ["SID"])
        
        pageData = resp.read()
        gv = _extractGV(pageData)

        self._cookieJar.addCookie("GV", gv)


    def _retrievePage(self, urlOrRequest):
        """
        """
        if not isinstance(urlOrRequest, urllib2.Request):
            req = urllib2.Request(urlOrRequest)
        else:
            req = urlOrRequest
            
        self._cookieJar.setCookies(req)
        resp = urllib2.urlopen(req)

        pageData = resp.read()

        # TODO: Do extract cookies here too?
        self._cookieJar.extractCookies(resp, [ACTION_TOKEN_COOKIE])

        # TODO: Enable logging of page data for debugging purposes?

        return pageData


    def _parsePage(self, urlOrRequest):
        """
        Retrieve & then parse the requested page content.
        
        """
        items = _parsePage(self._retrievePage(urlOrRequest))
        
        # Automatically cache some things like quota usage.
        # TODO: Cache more?
        # TODO: Expire cached values?
        # TODO: Do this better.
        try:
            self._cachedQuotaInfo = items[D_QUOTA]
        except KeyError:
            pass

        try:
            self._cachedLabelNames = [category[CT_NAME]
                                         for category in items[D_CATEGORIES]]
        except KeyError:
            pass
        
        return items


    def _parseSearchResult(self, searchType, start = 0, **kwargs):
        """
        """
        params = {U_SEARCH: searchType,
                  U_START: start,
                  U_VIEW: U_THREADLIST_VIEW,
                  }
        params.update(kwargs)
        
        return self._parsePage(_buildURL(**params))


    def _parseThreadSearch(self, searchType, allPages = False, **kwargs):
        """

        Only works for thread-based results at present. # TODO: Change this?
        """
        start = 0
        threadsInfo = []

        # Option to get *all* threads if multiple pages are used.
        while (start == 0) or (allPages and
                               len(threadsInfo) < threadListSummary[TS_TOTAL]):
            
                items = self._parseSearchResult(searchType, start, **kwargs)

                #TODO: Handle single & zero result case better? Does this work?
                try:
                    threads = items[D_THREAD]
                except KeyError:
                    break
                else:
                    if type(threads[0]) not in [tuple, list]:#TODO:Urgh,change!
                        threadsInfo.append(threads)
                    else:
                        # Note: This also handles when more than one "t"
                        # "DataPack" is on a page.
                        threadsInfo.extend(_splitBunches(threads))

                    # TODO: Check if the total or per-page values have changed?
                    threadListSummary = items[D_THREADLIST_SUMMARY]
                    threadsPerPage = threadListSummary[TS_NUM]

                    start += threadsPerPage

        # TODO: Record whether or not we retrieved all pages..?
        return GmailSearchResult(self, (searchType, kwargs), threadsInfo)


    def _retrieveJavascript(self, version = ""):
        """

        Note: `version` seems to be ignored.
        """
        return self._retrievePage(_buildURL(view = U_PAGE_VIEW,
                                            name = "js",
                                            ver = version))
        
        
    def getMessagesByFolder(self, folderName, allPages = False):
        """

        Folders contain conversation/message threads.

          `folderName` -- As set in Gmail interface.

        Returns a `GmailSearchResult` instance.
        """
        return self._parseThreadSearch(folderName, allPages = allPages)

    
    def getQuotaInfo(self, refresh = False):
        """

        Return MB used, Total MB and percentage used.
        """
        # TODO: Change this to a property.
        if not self._cachedQuotaInfo or refresh:
            # TODO: Handle this better...
            self.getMessagesByFolder(U_INBOX_SEARCH)

        return self._cachedQuotaInfo[:3]


    def getLabelNames(self, refresh = False):
        """
        """
        # TODO: Change this to a property?
        if not self._cachedLabelNames or refresh:
            # TODO: Handle this better...
            self.getMessagesByFolder(U_INBOX_SEARCH)

        return self._cachedLabelNames


    def getMessagesByLabel(self, label, allPages = False):
        """
        
        """
        return self._parseThreadSearch(U_CATEGORY_SEARCH,
                                       cat=label, allPages = allPages)


    def getRawMessage(self, msgId):
        """
        """
        return self._retrievePage(
            _buildURL(view=U_ORIGINAL_MESSAGE_VIEW, th=msgId))


    def getUnreadMsgCount(self):
        """
        """
        # TODO: Clean up queries a bit..?
        items = self._parseSearchResult(U_QUERY_SEARCH,
                                        q = "is:" + U_AS_SUBSET_UNREAD)

        return items[D_THREADLIST_SUMMARY][TS_TOTAL_MSGS]


    def sendMessage(self, msg):
        """

          `msg` -- `GmailComposedMessage` instance.
        
        """
        try:
            at = self._cookieJar._cookies[ACTION_TOKEN_COOKIE]
        except KeyError:
            self.getLabelNames(True) 
            at = self._cookieJar._cookies[ACTION_TOKEN_COOKIE]           

        params = {U_VIEW: U_SENDMAIL_VIEW,
                  U_REFERENCED_MSG: "",
                  U_THREAD: "",
                  U_DRAFT_MSG: "",
                  U_COMPOSEID: "1",
                  U_ACTION_TOKEN: at,
                  U_COMPOSE_TO: msg.to,
                  U_COMPOSE_CC: msg.cc,
                  U_COMPOSE_BCC: msg.bcc,
                  "subject": msg.subject,
                  "msgbody": msg.body,
                  }

        # Amongst other things, I used the following post to work out this:
        # <http://groups.google.com/groups?
        #  selm=mailman.1047080233.20095.python-list%40python.org>
        mimeMessage = _paramsToMime(params)

        # TODO: Tidy all this up.
        lines = mimeMessage.as_string().split("\n")

        contentTypeHeader = lines[0].split(": ", 1)
        data = "\r\n".join(lines[2:]) + "\r\n" # TODO: Use epilogue instead?
        
        req = urllib2.Request(_buildURL(search = "undefined"), data = data)
        req.add_header(*contentTypeHeader)

        items = self._parsePage(req)

        # TODO: Check composeid & store new thread id?
        return (items[D_SENDMAIL_RESULT][SM_SUCCESS] == 1)

        

def _splitBunches(infoItems):
    """

    Utility to help make it easy to iterate over each item separately,
    even if they were bunched on the page.
    """
    result= []

    # TODO: Decide if this is the best approach.
    for group in infoItems:
        if type(group) == tuple:
            result.extend(group)
        else:
            result.append(group)

    return result
            
        

class GmailSearchResult:
    """
    """

    def __init__(self, account, search, threadsInfo):
        """

        `threadsInfo` -- As returned from Gmail but unbunched.
        """
        self._account = account
        self.search = search # TODO: Turn into object + format nicely.

        self._threads = [GmailThread(self, thread)
                         for thread in threadsInfo]


    def __iter__(self):
        """
        """
        return iter(self._threads)


    def __len__(self):
        """
        """
        return len(self._threads)



class GmailThread:
    """



    Note: As far as I can tell, the "canonical" thread id is always the same
          as the id of the last message in the thread. But it appears that
          the id of any message in the thread can be used to retrieve
          the thread information.
    
    """

    def __init__(self, parent, threadInfo):
        """
        """
        self._parent = parent
        
        self.id = threadInfo[T_THREADID] # TODO: Change when canonical updated?
        self.subject = threadInfo[T_SUBJECT_HTML]

        # TODO: Store other info?
        # Extract number of messages in thread/conversation.

        self._authors = threadInfo[T_AUTHORS_HTML]

        try:
            # TODO: Find out if this information can be found another way...
            #       (Without another page request.)
            self._length = int(re.search("\((\d+?)\)\Z",
                                         self._authors).group(1))
        except AttributeError:
            # If there's no message count then the thread only has one message.
            self._length = 1

        # TODO: Store information known about the last message  (e.g. id)?
        self._messages = []
        

    def __len__(self):
        """
        """
        return self._length


    def __iter__(self):
        """
        """
        if not self._messages:
            self._messages = self._getMessages(self)
            
        return iter(self._messages)


    def _getMessages(self, thread):
        """
        """
        # TODO: Do this better.
        # TODO: Specify the query folder using our specific search?
        items = self._parent._account._parseSearchResult(U_QUERY_SEARCH,
                                                 view = U_CONVERSATION_VIEW,
                                                         th = thread.id,
                                                         q = "in:anywhere")

        # TODO: Handle this better?
        msgsInfo = items[D_MSGINFO]

        # TODO: Handle special case of only one message in thread better?
        if type(msgsInfo) != type([]):
            msgsInfo = [msgsInfo]

        return [GmailMessage(thread, msg)
                for msg in msgsInfo]

        
class GmailMessage(object):
    """
    """
    
    def __init__(self, thread, msgData):
        """
        """
        self._thread = thread
        
        self.id = msgData[MI_MSGID]
        self.number = msgData[MI_NUM]
        self.subject = msgData[MI_SUBJECT]

        # TODO: Populate additional fields & cache...(?)

        self._source = None


    def _getSource(self):
        """
        """
        if not self._source:
            # TODO: Ummm, do this a *little* more nicely...
            self._source = self._thread._parent._account.getRawMessage(self.id)

        return self._source

    source = property(_getSource, doc = "")
        

class GmailComposedMessage:
    """
    """

    def __init__(self, to, subject, body, cc = None, bcc = None):
        """
        """
        self.to = to
        self.subject = subject
        self.body = body
        self.cc = cc
        self.bcc = bcc



if __name__ == "__main__":
    import sys
    from getpass import getpass

    try:
        name = sys.argv[1]
    except IndexError:
        name = raw_input("Gmail account name: ")
        
    pw = getpass("Password: ")

    ga = GmailAccount(name, pw)

    print "\nPlease wait, logging in..."

    ga.login()

    print "Log in successful.\n"

    # TODO: Use properties instead?
    quotaInfo = ga.getQuotaInfo()
    quotaMbUsed = quotaInfo[QU_SPACEUSED]
    quotaMbTotal = quotaInfo[QU_QUOTA]
    quotaPercent = quotaInfo[QU_PERCENT]
    print "%s of %s used. (%s)\n" % (quotaMbUsed, quotaMbTotal, quotaPercent)

    searches = STANDARD_FOLDERS + ga.getLabelNames()

    while 1:
        try:
            print "Select folder or label to list: (Ctrl-C to exit)"
            for optionId, optionName in enumerate(searches):
                print "  %d. %s" % (optionId, optionName)

            name = searches[int(raw_input("Choice: "))]

            if name in STANDARD_FOLDERS:
                result = ga.getMessagesByFolder(name, True)
            else:
                result = ga.getMessagesByLabel(name, True)

            print
            if len(result):
                for thread in result:
                    print
                    print thread.id, len(thread), thread.subject
                    for msg in thread:
                        print "  ", msg.id, msg.number, msg.subject
                        #print msg.source
            else:
                print "No threads found in `%s`." % name

            print
        except KeyboardInterrupt:
            print "\n\nDone."
            break
