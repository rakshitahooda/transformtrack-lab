"""Mask-overlap transformation proposals for an original synthetic demo."""
from __future__ import annotations
from dataclasses import dataclass
import cv2
import numpy as np

H, W = 120, 180
@dataclass(frozen=True)
class Instance:
    key: str
    label: str
    mask: np.ndarray

def _draw(frame: int) -> np.ndarray:
    """Generate a binary lantern mask with a deterministic cap split and merge."""
    m = np.zeros((H, W), np.uint8)
    split = 3 <= frame <= 5
    body_x = 82 if split else 90 + (frame >= 6) * 2
    cap_y0, cap_y1 = (17, 32) if split else (25, 40)
    cv2.rectangle(m, (body_x-27, 48), (body_x+27, 91), 1, -1)
    cv2.rectangle(m, (body_x-20, 36), (body_x+20, 52), 1, -1)
    cv2.rectangle(m, (body_x-32, 89), (body_x+32, 96), 1, -1)
    cv2.rectangle(m, (body_x-24, cap_y0), (body_x+24, cap_y1), 1, -1)
    return m

def _instances(mask: np.ndarray, frame: int) -> list[Instance]:
    found=[]
    count, components, stats, centroids = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8), 8)
    parts=[]
    for n in range(1,count):
        if stats[n,cv2.CC_STAT_AREA] >= 20:
            parts.append((n, int(stats[n,cv2.CC_STAT_AREA])))
    for n, area in parts:
        label = "lantern"
        if 3 <= frame <= 5 and len(parts) == 2:
            label = "removable cap" if centroids[n,1] < 38 else "lantern body"
        found.append(Instance(f"f{frame}-{n}", label, components==n))
    return found

def _measure(a,b):
    inter=int(np.logical_and(a,b).sum()); aa=int(a.sum()); bb=int(b.sum())
    return {"pixels":inter,"iou":round(inter/(aa+bb-inter),3) if aa+bb>inter else 0.0,
            "old_coverage":inter/aa if aa else 0.0,"new_coverage":inter/bb if bb else 0.0}

def infer_transition(previous,current,min_coverage=.08):
    """Propose split/merge from pairwise mask coverage; scores are mean pair IoU."""
    previous,current=list(previous),list(current); links={}
    for i,a in enumerate(previous):
        for j,b in enumerate(current):
            score=_measure(a.mask,b.mask)
            if score['pixels'] and max(score['old_coverage'],score['new_coverage']) >= min_coverage:
                links[i,j]=score
    events=[]
    for i,a in enumerate(previous):
        js=[j for (pi,j),s in links.items() if pi==i and s['old_coverage']>=min_coverage]
        if len(js)>1:
            events.append({"kind":"split","from":[a.key],"to":[current[j].key for j in js],"labels":[current[j].label for j in js],"score":round(float(np.mean([links[i,j]['iou'] for j in js])),3),"evidence":[links[i,j] for j in js]})
    for j,b in enumerate(current):
        ii=[i for (i,cj),s in links.items() if cj==j and s['new_coverage']>=min_coverage]
        if len(ii)>1:
            events.append({"kind":"merge","from":[previous[i].key for i in ii],"to":[b.key],"labels":[b.label],"score":round(float(np.mean([links[i,j]['iou'] for i in ii])),3),"evidence":[links[i,j] for i in ii]})
    return events

LABELS=["Assembled","Stable track","Cap starts to move","Split proposal","Parts tracked","Reassembly proposal","Merged state","Identity updated"]
DESCRIPTIONS=["One synthetic lantern instance is visible.","The complete silhouette stays stable.","The cap begins to separate from the body.","One prior mask overlaps two current components.","Body and cap persist as distinct instances.","Two tracked parts overlap one newly assembled mask.","The merge is supported by pixel overlap.","The state graph advances after the proposal."]
MOTIONS=["track","track","candidate","split","track","candidate","merge","track"]
def build_demo():
    states=[]
    for i in range(8):
        instances=_instances(_draw(i),i)
        states.append({"index":i,"title":LABELS[i],"description":DESCRIPTIONS[i],"motion":MOTIONS[i],"phase":i/7,"objects":[{"id":x.key,"label":x.label,"area":int(x.mask.sum())} for x in instances],"_instances":instances})
    events=[]
    for i in range(1,len(states)):
        for e in infer_transition(states[i-1]['_instances'],states[i]['_instances']):
            e.update(frame=i,time=round(i*.75,2),from_title=states[i-1]['title'],to_title=states[i]['title']);events.append(e)
    return {"states":[{k:v for k,v in s.items() if not k.startswith('_')} for s in states],"events":events,
      "graph":{"nodes":[{"id":f"s{s['index']}","label":s['title'],"objects":[o['label'] for o in s['objects']]} for s in states],"edges":[{"from":f"s{e['frame']-1}","to":f"s{e['frame']}","kind":e['kind'],"score":e['score']} for e in events]},
      "summary":{"frames":len(states),"events":len(events),"splits":sum(e['kind']=='split' for e in events),"merges":sum(e['kind']=='merge' for e in events)}}
def make_mask(index):
    if not 0<=index<8: raise ValueError('frame index must be 0..7')
    return _draw(index)
