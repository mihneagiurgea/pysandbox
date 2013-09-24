import sys
ls=open(sys.argv[1]).readlines()
N=int(ls[0])
cs=[l.strip() for l in ls[1:N+1]]
vs={}
for l in ls[N+2:]:
    c,n=l.split()
    if c in cs:
        vs[c]=vs.get(c, 0) + int(n)
mvs=max(vs.values())
p=100.0*mvs/sum(vs.values())
for c, n in sorted(vs.items()):
    if n==mvs:
        print '%s %.2f' % (c, p)
