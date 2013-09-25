def pop_min(s1, s2, reserved=0):
    min_el = None
    while len(s1) > reserved:
        el = s1.pop()
        if min_el is None:
            min_el = el
        elif el < min_el:
            s2.append(min_el)
            min_el = el
        else:
            s2.append(el)
    return min_el

def pour(s1, s2):
    while len(s1) > 0:
        s2.append(s1.pop())

def sort_stack(s1, s2):
    N = len(s1)
    for reserved in xrange(N):
        min_el = pop_min(s1, s2, reserved)
        s1.append(min_el)
        pour(s2, s1)

s1 = [4 , 6, 2, 1, 5]
s2 = []
sort_stack(s1, s2)
print s1
print s2