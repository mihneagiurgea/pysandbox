import glob
import lxml.html


class Result(object):

    def __init__(self, time, title, score, odds):
        self.time = time
        self.title = title
        self.score = score
        self.odds = tuple(odds)
        x, y = map(int, score.split(':'))
        if x == y:
            self.outcome = 1
        elif x > y:
            self.outcome = 0
        else:
            self.outcome = 2

    def __str__(self):
        return '%(time)s %(title)s %(score)s %(odds)s %(outcome)s' % self.__dict__

    @property
    def odds1(self):
        return self.odds[0]

    @property
    def oddsx(self):
        return self.odds[1]

    @property
    def odds2(self):
        return self.odds[2]

def parse_row(row):
    if 'deactivate' not in row.get('class'):
        return None
    tds = list(row.iterchildren())
    assert(len(tds) == 7)

    # print [td.text_content() for td in tds]

    # ['20:00', 'Crystal Palace - West Ham', '1:0', '3.15', '3.25', '2.37', '19']
    time = tds[0].text_content()
    title = tds[1].text_content()
    score = tds[2].text_content()
    odds = []
    outcome = None
    for i in (3, 4, 5):
        odds.append(float(tds[i].text_content()))
        if 'result-ok' in tds[i].get('class'):
            assert outcome is None
            outcome = i - 3
    # if outcome is None:
        # raise ValueError('Invalid row: %r' % [td.text_content() for td in tds])
    # assert(outcome is not None)
    # Convert (0, 1, 2) -> (1, X, 2)
    # if outcome == 0:
    #     outcome = 1
    # elif outcome == 1:
    #     outcome = 'X'
    # else:
    #     outcome = 2
    return Result(time, title, score, odds)

def parse_results(filename):
    content = open(filename).read()
    html = lxml.html.fromstring(content)
    table = html.get_element_by_id('tournamentTable')
    tbody = list(table.iterchildren())[1]
    rows = tbody.iterchildren()
    results = []
    for row in rows:
        result = parse_row(row)
        if result is not None:
            results.append(result)
    return results

def parse_all_html(pattern):
    results = []
    for filename in glob.glob(pattern):
        # print filename
        results.extend(parse_results(filename))
    return results

def make_bet(result, lower_cutoff=6.0, upper_cutoff=8.0):
    bet = 0
    count = 0

    max_odd = max(result.odds)
    if lower_cutoff < max_odd < upper_cutoff:
        i = result.odds.index(max_odd)

        amount = 1.0
        bet -= amount
        if result.outcome == i:
            bet += amount * result.odds[i]
        count += 1

    # bet = 0
    # count = 0
    # for i in range(3):
    #     if lower_cutoff < result.odds[i] < upper_cutoff:
    #         amount = 1.0
    #         count += 1
    #         bet -= amount
    #         if result.outcome == i:
    #             bet += amount * result.odds[i]
    # # if count > 1:
    #     # print result

    return (bet, count)

def make_all_bets(results, lower_cutoff=6.0, upper_cutoff=8.0):
    total = 0
    count = 0
    for result in results:
         x, y = make_bet(result, lower_cutoff, upper_cutoff)
         total += x
         count += y
    return total, count

if __name__ == '__main__':
    results = parse_all_html('/Users/skip/Dropbox/Pariuri/201*.html')
    print make_all_bets(results, 3.0, 3.5)

    # # results = parse_all_html('/Users/skip/Dropbox/Pariuri/*.html')
    print 'Total of %d results' % len(results)

    STEP = 0.25
    l = 1.0
    while l < 10.0:
        u = l + 2 * STEP
        while u < 10.0:
            expected, count = make_all_bets(results, l, u)
            if expected > 0:
                print '[%.2f-%.2f] => %+.4f (%d bets)' % (l, u, expected, count)
                # print '%.2f' % x,
            u += STEP
        # print
        l += STEP
