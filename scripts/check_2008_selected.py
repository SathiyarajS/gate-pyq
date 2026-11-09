#!/usr/bin/env python3
"""Selected finite checks, not official-key verification."""
from itertools import product
# Printed product table: independently form the four Cartesian states.
y={(1,'a'):1,(1,'b'):2,(2,'a'):2,(2,'b'):1}
z={(1,'a'):2,(1,'b'):2,(2,'a'):1,(2,'b'):1}
states={'P':(1,1),'Q':(1,2),'R':(2,2),'S':(2,1)}; names={v:k for k,v in states.items()}
rows={name:tuple(names[z[a,c],y[b,c]] for c in 'ab') for name,(a,b) in states.items()}
assert rows=={'P':('S','R'),'Q':('R','S'),'R':('Q','P'),'S':('P','Q')}
# Missing option in Q79.
valid=[''.join(x) for x in product('01',repeat=5) if '00' not in ''.join(x)]
assert len(valid)==13
# Q75 value recurrence.
a=[0,1]
for n in range(2,9):a.append(2*a[-1]+3*a[-2])
assert a[8]==1640
# Proposed repair A in Q85 still misses a singleton.
y=list(range(1,11));x=4;i=0;j=9
while True:
 k=(i+j)//2
 if y[k]<x:i=k+1
 else:j=k-1
 if not(y[k]!=x and i<j):break
assert y[k]!=x and x in y
print('PASS: product table, 32 binary strings, recurrence1640 and binary-search singleton counterexample.')
