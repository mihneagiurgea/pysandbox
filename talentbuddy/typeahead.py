class TrieNode(object):

    def __init__(self):
        self.value = -1
        self.min_char = None
        self.children = {}

    def insert(self, word, value):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
                if node.min_char is None or char < node.min_char:
                    node.min_char = char
            node = node.children[char]
        node.value = value

    def lookup(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def find_first_word(self):
        node = self
        while node.value == -1:
            node = node.children[node.min_char]
        return node

def typeahead(usernames, queries):
    trie = TrieNode()
    for i, username in enumerate(usernames):
        trie.insert(username.lower(), i)
    for query in queries:
        node = trie.lookup(query.lower())
        if node is None:
            print -1
        else:
            node = node.find_first_word()
            print usernames[node.value]

if __name__ == '__main__':
    usernames = ["james", "jBlank"]
    queries = ["j", "jm", "jbl", "JB"]
    typeahead(usernames, queries)