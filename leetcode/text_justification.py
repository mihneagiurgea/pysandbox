def full_justify(words, L):

    def justify_current_line():
        if len(current_words) == 1:
            word = current_words[0]
            return word + ' ' * (L - len(word))
        else:
            remaining_spaces = L - S
            M = len(current_words) - 1

            pieces = [current_words[0]]
            for i in range(M):
                nr_spaces = remaining_spaces / M
                if i < remaining_spaces % M:
                    nr_spaces += 1
                pieces.append(' ' * nr_spaces)
                pieces.append(current_words[i+1])
            return ''.join(pieces)

    lines = []

    current_words = []
    # S = sum(w.length for w in current_words)
    S = 0
    for word in words:
        if S + len(word) + max(len(current_words) - 1, 0) <= L:
            # Add word to current line.
            current_words.append(word)
            S += len(word)
        else:
            # Flush current line.
            lines.append(justify_current_line())
            current_words = [word]
            S = len(word)

    if current_words:
        lines.append(' '.join(current_words))

    return lines

words = ["This", "is", "an", "example", "of", "text", "justification.",
        "Poponetz"]
L = 16
print '\n'.join(full_justify(words, L))