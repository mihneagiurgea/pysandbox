import doctest


class Trie(object):
    """
    >>> t = Trie()
    >>> t.add("cat")
    >>> t.add("car")
    >>> t.add("carton")
    >>> t.add("orange")
    >>> t.longest_prefix("casualty")
    'ca'
    >>> t.longest_prefix("orange")
    'orange'
    >>> t.longest_prefix("ora")
    'ora'
    """

    def __init__(self):
        # c -> a -> t
        #        -> r
        #        -> c
        # "t" {t: None}
        self._t = {}

    def add(self, word):
        self._recursive_add(self._t, word)

    def _recursive_add(self, d, word):
        if not word:
            return

        first_letter = word[0]
        if first_letter not in d:
            d[first_letter] = {}
            self._recursive_add(d[first_letter], word[1:])

    def longest_prefix(self, word):
        return self._query(self._t, word)

    def _query(self, node, word):
        if not word:
            return ""

        first_letter = word[0]
        if first_letter in node:
            return first_letter + self._query(node[first_letter], word[1:])
        else:
            return ""


doctest.testmod()
