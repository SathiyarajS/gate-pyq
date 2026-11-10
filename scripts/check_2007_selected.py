#!/usr/bin/env python3
"""Finite checks for selected 2007 solutions, not official-key comparisons."""
from functools import lru_cache
from math import comb
# Source grammar, count parse trees by substring.
g={'S':['aB','bA'],'A':['a','aS','bAA'],'B':['b','bS','aBB']}
@lru_cache(None)
def count(nt,s):
 ans=0
 for rhs in g[nt]:
  if not s or s[0]!=rhs[0]:continue
  rest=s[1:]
  if len(rhs)==1:ans+=not rest
  elif len(rhs)==2:ans+=count(rhs[1],rest)
  else:ans+=sum(count(rhs[1],rest[:i])*count(rhs[2],rest[i:]) for i in range(1,len(rest)))
 return ans
assert count('S','aabbab')==2
# Direct-mapped cache, two sequential byte scans.
lines=[None]*32;miss=0
for _ in range(2):
 for a in range(0x1100,0x1100+2500):
  b=a//64;i=b%32
  if lines[i]!=b:miss+=1;lines[i]=b
assert miss==56
# CRC codeword divisibility.
x=int('11001001011',2);gpoly=0b1001
while x.bit_length()>=gpoly.bit_length():x^=gpoly<<(x.bit_length()-gpoly.bit_length())
assert x==0
assert comb(20,10)-comb(8,4)*comb(11,5)==152416
# Literal source-minus-destination instruction algebra on finite inputs.
from itertools import product
for a,b,c,d,e in product(range(-2,3),repeat=5):
 target=(a+b)-(e-(c+d));r=0;r=c+r;r=d+r;r=e-r;r=a-r;r=b+r
 assert r==target
print('PASS: grammar two trees, cache56, CRC, lattice152416, 3125 MOV-reassociation examples.')
