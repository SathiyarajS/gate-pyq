#!/usr/bin/env python3
"""Finite arithmetic/algorithm checks; not official-key verification."""
import heapq
from fractions import Fraction
assert ((400*20)+16)*63+29==505037
assert divmod(1039,1260)==(0,1039)
assert divmod(1039,63)==(16,31)
a=[25,14,16,13,10,8,12]
for _ in range(2):
 a[0]=a.pop();i=0
 while 2*i+1<len(a):
  j=2*i+1
  if j+1<len(a) and a[j+1]>a[j]:j+=1
  if a[i]>=a[j]:break
  a[i],a[j]=a[j],a[i];i=j
assert a==[14,13,12,8,10]
# LCS implementations in both valid topological fill orders.
def lcs(x,y,column=False):
 a=[[0]*(len(y)+1) for _ in range(len(x)+1)]
 cells=[(i,j) for i in range(1,len(x)+1) for j in range(1,len(y)+1)]
 if column:cells.sort(key=lambda z:(z[1],z[0]))
 for i,j in cells:a[i][j]=a[i-1][j-1]+1 if x[i-1]==y[j-1] else max(a[i-1][j],a[i][j-1])
 return a[-1][-1]
from itertools import product
strings=[''.join(x) for n in range(5) for x in product('ab',repeat=n)]
for x in strings:
 for y in strings:assert lcs(x,y)==lcs(x,y,True)
# Q55 mixed supplier demonstrates the literal option/query difference.
colors={'mixed':{'blue','red'},'red':{'red'},'blue':{'blue'},'none':set()}
query={s for s,v in colors.items() if 'blue' not in v}
literal_not_only_blue={s for s,v in colors.items() if not(v and v<={'blue'})}
assert query=={'red','none'} and 'mixed' in literal_not_only_blue-query
print('PASS: disk arithmetic, two heap deletions, 961 LCS fill-order comparisons and SQL wording counterexample.')
print('Q47 exact TCP forbidden-region bound is not certified by this script.')
