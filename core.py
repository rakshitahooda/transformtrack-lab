"""Synthetic mask sequence and transparent split/merge proposals for TransformTrack Lab."""
from __future__ import annotations
from dataclasses import dataclass
import base64
import cv2
import numpy as np

H, W = 160, 240
@dataclass(frozen=True)
class Instance:
    key: str
    label: str
    mask: np.ndarray


def _draw(frame: int) -> np.ndarray:
    """Create a deterministic overhead view mask of a travel mug and loose lid."""
    m = np.zeros((H, W), np.uint8)
    separated = 3 <= frame <= 5
    dx = -8 if separated else 0
    # Body and handle form one connected component.
    cv2.fillPoly(m, [np.array([[83+dx, 62], [157+dx, 62], [148+dx, 132], [92+dx, 132]], np.int32)], 1)
    cv2.ellipse(m, (156+dx, 94), (22, 22), 0, 0, 360, 1, 5)
    # Lid is attached when assembled and floats above the rim when removed.
    lid_y = 50 if separated else 54
    cv2.rectangle(m, (79+dx, lid_y), (161+dx, lid_y+9), 1, -1)
    cv2.rectangle(m, (91+dx, lid_y-7), (149+dx, lid_y), 1, -1)
    if separated:
        # Small steam/button nub belongs to the lid and stays connected.
        cv2.rectangle(m, (111+dx, lid_y-12), (129+dx, lid_y-7), 1, -1)
    return m


def _instances(mask: np.ndarray, frame: int) -> list[Instance]:
    count, labels, stats, centroids = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8), 8)
    components=[]
    for n in range(1, count):
        if stats[n, cv2.CC_STAT_AREA] >= 20:
            components.append((n, int(stats[n, cv2.CC_STAT_AREA])))
    parts=[]
    separated = 3 <= frame <= 5 and len(components) == 2
    for n, area in sorted(components, key=lambda item: centroids[item[0], 1]):
        label = ("loose lid", "mug body")[int(centroids[n,1] > 52)] if separated else "travel mug"
        # IDs are deliberately explanatory synthetic track labels, not learned identities.
        if separated:
            key = "T02" if label == "loose lid" else "T01"
        else:
            key = "T03" if frame >= 6 else "T01"
        parts.append(Instance(key, label, labels == n))
    return parts


def _measure(a: np.ndarray, b: np.ndarray) -> dict:
    inter=int(np.logical_and(a,b).sum()); aa=int(a.sum()); bb=int(b.sum())
    union=aa+bb-inter
    return {"pixels":inter,"iou":round(inter/union,3) if union else 0.0,
            "old_coverage":inter/aa if aa else 0.0,"new_coverage":inter/bb if bb else 0.0}


def infer_transition(previous, current, min_coverage=.08):
    """Use mask overlap to propose splits/merges; this is not semantic validation."""
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
            events.append({"kind":"split","from":[a.key],"to":[current[j].key for j in js],"labels":[current[j].label for j in js],"score":round(float(np.mean([links[i,j]['iou'] for j in js])),3),"evidence":[{"from":a.key,"to":current[j].key,**links[i,j]} for j in js]})
    for j,b in enumerate(current):
        ii=[i for (i,cj),s in links.items() if cj==j and s['new_coverage']>=min_coverage]
        if len(ii)>1:
            events.append({"kind":"merge","from":[previous[i].key for i in ii],"to":[b.key],"labels":[b.label],"score":round(float(np.mean([links[i,j]['iou'] for i in ii])),3),"evidence":[{"from":previous[i].key,"to":b.key,**links[i,j]} for i in ii]})
    return events

LABELS=["One mug, one identity","The mug stays together","The lid begins to lift","Two pieces, two tracks","The lid remains separate","The pieces move back together","One mug shape returns","A new whole-object track"]
DESCRIPTIONS=["A synthetic travel mug starts as one connected mask.","The same mug is still one component; its track stays T01.","The lid moves away from the cup. The next frame tests for a split.","Two disconnected masks overlap the earlier mug mask: body T01 and lid T02.","The two component masks persist as separate synthetic tracks.","The lid comes back over the cup; overlap proposes a merge.","The pieces form one connected mask again.","The reassembled mug receives a new illustrative track ID, T03."]
MOTIONS=["track","track","candidate","split","track","candidate","merge","track"]


def _mask_data(mask: np.ndarray, color: tuple[int, int, int]) -> str:
    """Encode a true per-instance synthetic mask with a colored transparent overlay."""
    rgba = np.zeros((H, W, 4), dtype=np.uint8)
    rgba[mask] = (*color, 118)
    ok, encoded = cv2.imencode(".png", rgba)
    if not ok:
        raise RuntimeError("could not encode synthetic mask")
    return "data:image/png;base64," + base64.b64encode(encoded.tobytes()).decode("ascii")


def build_demo():
    states=[]
    for i in range(8):
        instances=_instances(_draw(i),i)
        states.append({"index":i,"title":LABELS[i],"description":DESCRIPTIONS[i],"motion":MOTIONS[i],"phase":i/7,"objects":[{"id":x.key,"label":x.label,"area":int(x.mask.sum()),"mask_png":_mask_data(x.mask,(32,166,161) if x.label=="loose lid" else (132,103,223) if x.label=="travel mug" else (222,128,77))} for x in instances],"_instances":instances})
    events=[]
    for i in range(1,len(states)):
        for e in infer_transition(states[i-1]['_instances'],states[i]['_instances']):
            e.update(frame=i,time=round(i*.8,2),from_title=states[i-1]['title'],to_title=states[i]['title']);events.append(e)
    branches=[
      {"id":"split-yes","frame":3,"kind":"split","selected":True,"title":"Body + lid","detail":"Two disconnected masks persist from the prior mug mask.","track_ids":["T01","T02"]},
      {"id":"split-alt","frame":3,"kind":"alternative","selected":False,"title":"Keep one mug","detail":"Not chosen in this toy sequence: the current mask has two components.","track_ids":["T01"]},
      {"id":"merge-yes","frame":6,"kind":"merge","selected":True,"title":"Reassembled mug","detail":"One connected mask overlaps both preceding part masks.","track_ids":["T03"]},
      {"id":"merge-alt","frame":6,"kind":"alternative","selected":False,"title":"Keep parts separate","detail":"Not chosen in this toy sequence: the components have become connected.","track_ids":["T01","T02"]}
    ]
    nodes=[
      {"id":"start","frame":0,"x":70,"y":150,"title":"Whole mug","subtitle":"T01 · one mask","type":"state","selected":True},
      {"id":"split","frame":3,"x":330,"y":82,"title":"Body + lid","subtitle":"T01 + T02","type":"state","selected":True},
      {"id":"split-alt","frame":3,"x":330,"y":220,"title":"Keep one mug","subtitle":"alternative","type":"alternative","selected":False},
      {"id":"parts","frame":4,"x":560,"y":82,"title":"Separate parts","subtitle":"two masks persist","type":"state","selected":True},
      {"id":"merge","frame":6,"x":800,"y":82,"title":"Reassembled","subtitle":"T03 · one mask","type":"state","selected":True},
      {"id":"merge-alt","frame":6,"x":800,"y":220,"title":"Keep parts","subtitle":"alternative","type":"alternative","selected":False}
    ]
    edges=[
      {"from":"start","to":"split","label":"split proposal","type":"accepted","frame":3},
      {"from":"start","to":"split-alt","label":"not selected","type":"alternative","frame":3},
      {"from":"split","to":"parts","label":"tracks persist","type":"accepted","frame":4},
      {"from":"parts","to":"merge","label":"merge proposal","type":"accepted","frame":6},
      {"from":"parts","to":"merge-alt","label":"not selected","type":"alternative","frame":6}
    ]
    return {"states":[{k:v for k,v in s.items() if not k.startswith('_')} for s in states],"events":events,
      "graph":{"nodes":nodes,"edges":edges,"branches":branches},
      "summary":{"frames":len(states),"events":len(events),"splits":sum(e['kind']=='split' for e in events),"merges":sum(e['kind']=='merge' for e in events)}}


def make_mask(index):
    if not 0<=index<8: raise ValueError('frame index must be 0..7')
    return _draw(index)
