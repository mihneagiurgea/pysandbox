def tokenize(text):
    return [token for token in text.split(' ') if token]

def extract_contexts(books, tweets, w):
    # Tokenize each tweet and each book.
    books = map(tokenize, books)
    tweets = map(tokenize, tweets)

    for book in books:
        for tweet in tweets:
            for i in range(len(tweet) - len(book) + 1):
                match = True
                for j in range(len(book)):
                    if tweet[i+j] != book[j]:
                        match = False
                        break

                if match:
                    # Found a match, print context.
                    j = i + len(book)
                    context = tweet[max(i-w, 0): i] + ['-TITLE-'] + tweet[j:j+w]
                    print ' '.join(context)
                    break

books = ["Up and Running", "HTML5 Cookbook"]
tweets = ["Did you read Up and Running ?",
    "Looking forward to the HTML5 Cookbook release",
    "Is Up and running of any good?",
    "Up and Running ,best book ever"]

extract_contexts(books, tweets, 3)