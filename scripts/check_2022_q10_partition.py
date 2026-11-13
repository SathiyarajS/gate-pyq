#!/usr/bin/env python3
"""Exact finite check for 2022 CS Q10 under pole-to-pole full-partition assumptions.

Constructs planar faces from all eligible pairs of added ropes, removes collinear
vertices, and compares exact rational consecutive-edge ratios up to rotation and
reflection. Existing ropes must be boundaries, not unused interior decorations.
This does not address arbitrary rope endpoints away from the pictured poles.
"""
import math,itertools
from fractions import Fraction as F
from functools import cmp_to_key
outer=[(0.,0.),(5.,0.),(6.,1.),(6.,6.),(1.,6.),(0.,5.)]
outer=[tuple(F(int(v)) for v in p) for p in outer]
border=list(zip(outer,outer[1:]+outer[:1]));fixed=[((0.,4.),(2.,4.)),((4.,0.),(4.,2.))];ends=[(2.,4.),(4.,2.)]
fixed=[tuple(tuple(F(int(v)) for v in p) for p in seg) for seg in fixed]
ends=[tuple(F(int(v)) for v in p) for p in ends]
points=[(F(x),F(y)) for x in range(7) for y in range(7) if y>=x-5 and y<=x+5]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def on(p,s):
 a,b=s;return cross(sub(p,a),sub(b,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
segments=[s for s in itertools.combinations(points,2) if not any(on(s[0],b) and on(s[1],b) for b in border)]
A={i for i,s in enumerate(segments) if on(ends[0],s)};B={i for i,s in enumerate(segments) if on(ends[1],s)}
pairs={tuple(sorted((i,j))) for i in A for j in B if i!=j}
pairs.update(tuple(sorted((i,j))) for i in A&B for j in range(len(segments)) if i!=j)
def rounded(p):return p
def faces(segs):
 cuts=[set(s) for s in segs]
 for i in range(len(segs)):
  a,b=segs[i];r=sub(b,a)
  for j in range(i):
   c,d=segs[j];v=sub(d,c);den=cross(r,v)
   if den==0:
    for p in (a,b,c,d):
     if on(p,segs[i]) and on(p,segs[j]):cuts[i].add(p);cuts[j].add(p)
   else:
    t=cross(sub(c,a),v)/den;u=cross(sub(c,a),r)/den
    if 0<=t<=1 and 0<=u<=1:
     p=rounded((a[0]+t*r[0],a[1]+t*r[1]));cuts[i].add(p);cuts[j].add(p)
 adj={}
 for cut in cuts:
  pts=sorted(cut)
  for a,b in zip(pts,pts[1:]):adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
 # A dangling fixed rope cannot be part of a valid full boundary partition.
 if any(len(v)==1 for v in adj.values()):return []
 def angle_cmp(u,v):
  hu=0 if u[1]>0 or (u[1]==0 and u[0]>=0) else 1
  hv=0 if v[1]>0 or (v[1]==0 and v[0]>=0) else 1
  if hu!=hv:return -1 if hu<hv else 1
  c=cross(u,v);return -1 if c>0 else (1 if c<0 else 0)
 for a,v in adj.items():adj[a]=sorted(v,key=cmp_to_key(lambda b,c:angle_cmp(sub(b,a),sub(c,a))))
 seen=set();out=[]
 for a in adj:
  for b in adj[a]:
   if (a,b) in seen:continue
   poly=[];u,v=a,b
   while (u,v) not in seen:
    seen.add((u,v));poly.append(u);w=adj[v][(adj[v].index(u)-1)%len(adj[v])];u,v=v,w
   area=sum(cross(x,y) for x,y in zip(poly,poly[1:]+poly[:1]))/2
   if area>0:
    # Remove straight continuation vertices.
    poly=[p for k,p in enumerate(poly) if cross(sub(p,poly[k-1]),sub(poly[(k+1)%len(poly)],p))!=0]
    out.append(poly)
 return out
def signature(poly):
 vals=[]
 for pp in (poly,list(reversed(poly))):
  e=[sub(pp[(i+1)%len(pp)],pp[i]) for i in range(len(pp))]
  seq=[]
  for i,u in enumerate(e):
   v=e[(i+1)%len(e)];norm=u[0]*u[0]+u[1]*u[1]
   seq.append(((u[0]*v[0]+u[1]*v[1])/norm,cross(u,v)/norm))
  for k in range(len(seq)):
   rotated=seq[k:]+seq[:k];vals.append(tuple(rotated));vals.append(tuple((a,-b) for a,b in rotated))
 return min(vals)
print('poles',len(points),'segments',len(segments),'candidate pairs',len(pairs),flush=True)
four=0;matches=[]
for i,j in sorted(pairs):
 fs=faces(border+fixed+[segments[i],segments[j]])
 if len(fs)==4:
  four+=1
  if len({signature(p) for p in fs})==1:matches.append((segments[i],segments[j]))
print('four-face pairs',four,'similar solutions',matches,flush=True)
assert not matches
construction=[((2.,4.),(2.,6.)),((4.,2.),(6.,2.)),((2.,4.),(4.,2.))]
construction=[tuple(tuple(F(int(v)) for v in p) for p in seg) for seg in construction]
fs=faces(border+fixed+construction);print('three-rope construction',fs,'similar',len(fs)==4 and len({signature(p) for p in fs})==1)

one_rope_count=sum(len(faces(border+fixed+[s]))==4 for s in segments)
print('one-rope four-face solutions',one_rope_count)
assert one_rope_count==0
assert len(fs)==4 and len({signature(p) for p in fs})==1
