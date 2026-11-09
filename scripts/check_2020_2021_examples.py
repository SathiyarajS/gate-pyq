#!/usr/bin/env python3
"""Finite checks supporting selected original derivations; not completeness proofs."""
from itertools import permutations, product
import re

# 2020 printed CS42: indistinguishable Ls, no character at its original position.
assert sum(all(a != b for a,b in zip(t,'LILAC')) for t in set(permutations('LILAC'))) == 12
# 2020 printed CS52: explicit seven-color edge coloring.
a_colors=[1,2,3]; b_colors=[4,5,6,7]
rows=[(2,3,4,5),(1,4,3,6),(5,1,2,4)]
for i,row in enumerate(rows):
 assert len(set(row+(a_colors[i],))) == 5
for j in range(4):
 assert len(set([rows[i][j] for i in range(3)]+[b_colors[j]])) == 4
# 2021 CS2 printed CS41: finite sanity check of four-run intersection formula.
for a,b,c,d in product(range(1,7),repeat=4):
 s='0'*a+'1'*b+'0'*c+'1'*d
 n=len(s)//2
 actual=len(s)%2==0 and any(s==s[:k]+s[k:n]+s[:k][::-1]+s[k:n][::-1] for k in range(n+1))
 predicted=(a==c and b>=d and (b-d)%2==0) or (b==d and c>=a and (c-a)%2==0)
 assert actual==predicted
# 2021 CS2 printed CS47: exhaustive finite check; automaton proof is in solution.
patterns=[r'(0|1(01*0)*1)*',r'(0|11|10(1|00)*01)*',r'(0*(1(01*0)*1)*)*']
for n in range(13):
 for t in product('01',repeat=n):
  s=''.join(t); expected=not s or int(s,2)%3==0
  assert all(bool(re.fullmatch(p,s))==expected for p in patterns)
# 2021 CS2 printed CS52: both the don't-care minimum and a fixed completion.
forced_on={0,1,6,7,8,9,11,13,14,15};forced_off={4,5,10}
for n in range(16):
 w,x,y,z=[bool(n & (1<<k)) for k in (3,2,1,0)]
 f=(not x and not y) or (x and y) or (w and z)
 assert n not in forced_on or f
 assert n not in forced_off or not f
 g=f or (not w and not x and not z)
 assert g == (n in forced_on|{2})
print('Selected 2020/2021 finite checks passed. See source-linked solutions for proofs and assumptions.')
