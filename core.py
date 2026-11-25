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


# Additional handcrafted case studies. These are illustrative masks, not inferred from the real footage.
def _rounded_mask(shape):
    m=np.zeros((H,W),np.uint8)
    x,y,w,h=map(int,(shape['x'],shape['y'],shape['w'],shape['h']))
    kind=shape['kind']
    if kind in ('battery','usb_connector'):
        cv2.rectangle(m,(x+min(w,h)//2,y),(x+w-min(w,h)//2,y+h),1,-1)
        cv2.ellipse(m,(x+min(w,h)//2,y+h//2),(min(w,h)//2,min(w,h)//2),0,0,360,1,-1)
        cv2.ellipse(m,(x+w-min(w,h)//2,y+h//2),(min(w,h)//2,min(w,h)//2),0,0,360,1,-1)
    else:
        r=max(2,min(8,h//5,w//5))
        cv2.rectangle(m,(x+r,y),(x+w-r,y+h),1,-1)
        cv2.rectangle(m,(x,y+r),(x+w,y+h-r),1,-1)
        for cx in (x+r,x+w-r):
            for cy in (y+r,y+h-r): cv2.circle(m,(cx,cy),r,1,-1)
    return m


def _graph(nodes, edges):
    return {'nodes':nodes,'edges':edges,'branches':[]}


def _case(case_id,title,description,scene,states,graph):
    out_states=[]; instances_by_state=[]
    colors={'body':(132,103,223),'cover':(32,166,161),'battery':(226,157,66),'connector':(72,160,204),'cap':(204,116,160),'whole':(132,103,223)}
    for i,s in enumerate(states):
        objects=[]; inst=[]
        for o in s['objects']:
            mask=_rounded_mask(o['shape'])
            key=o['id']; label=o['label']
            inst.append(Instance(key,label,mask.astype(bool)))
            color=colors.get(o.get('color_role','body'),(132,103,223))
            objects.append({'id':key,'label':label,'area':int(mask.sum()),'mask_png':_mask_data(mask.astype(bool),color),'shape':o['shape'],'color_role':o.get('color_role','body')})
        out_states.append({'index':i,'title':s['title'],'description':s['description'],'motion':s.get('motion','track'),'objects':objects})
        instances_by_state.append(inst)
    events=[]
    for i in range(1,len(out_states)):
        proposed=infer_transition(instances_by_state[i-1],instances_by_state[i],min_coverage=.04)
        focus=states[i].get('motion')
        for e in proposed:
            if focus not in ('split','merge') or e['kind'] != focus: continue
            e.update(frame=i,time=round(i*.8,2),from_title=out_states[i-1]['title'],to_title=out_states[i]['title'])
            events.append(e)
    return {'id':case_id,'title':title,'description':description,'scene':scene,'states':out_states,'events':events,'graph':graph,
            'summary':{'frames':len(out_states),'events':len(events),'splits':sum(e['kind']=='split' for e in events),'merges':sum(e['kind']=='merge' for e in events)}}


def _remote_case():
    def whole(): return {'id':'T05','label':'TV remote · assembled','color_role':'whole','shape':{'kind':'roundrect','x':65,'y':17,'w':104,'h':116}}
    def body(): return {'id':'T01','label':'Remote shell','color_role':'body','shape':{'kind':'roundrect','x':65,'y':18,'w':70,'h':105}}
    def cover(x=130,y=28): return {'id':'T02','label':'Battery cover','color_role':'cover','shape':{'kind':'roundrect','x':x,'y':y,'w':39,'h':70}}
    def cell(which,x,y): return {'id':which,'label':'AAA battery '+('A' if which=='T03' else 'B'),'color_role':'battery','shape':{'kind':'battery','x':x,'y':y,'w':15,'h':36}}
    states=[
      {'title':'Remote assembled','description':'One synthetic silhouette represents the complete remote before opening.','motion':'track','objects':[whole()]},
      {'title':'Cover slides away','description':'The rear cover separates from the remote shell; track continuity is an illustrative hypothesis.','motion':'split','objects':[body(),cover(130,29),cell('T03',82,48),cell('T04',103,48)]},
      {'title':'Cells lifted out','description':'The battery bay is visible, with two AAA cells shown as separate components.','motion':'split','objects':[body(),cover(130,27),cell('T03',78,126),cell('T04',101,126)]},
      {'title':'One cell removed','description':'Cell A is off the remote; Cell B remains in the open compartment.','motion':'track','objects':[body(),cover(130,27),cell('T03',45,130),cell('T04',101,51)]},
      {'title':'Both cells out','description':'Two loose batteries sit beside the open shell and cover.','motion':'track','objects':[body(),cover(130,27),cell('T03',45,130),cell('T04',72,130)]},
      {'title':'Cells returned','description':'Both cells are back in the bay; the detached cover remains a separate part.','motion':'track','objects':[body(),cover(130,27),cell('T03',78,48),cell('T04',101,48)]},
      {'title':'Cover closes','description':'The cover meets the shell. A merge is proposed from overlapping synthetic masks.','motion':'merge','objects':[whole()]},
      {'title':'Remote reassembled','description':'The sequence ends with one complete remote-control silhouette.','motion':'track','objects':[whole()]},
    ]
    nodes=[{'id':'r0','frame':0,'x':24,'y':108,'title':'Remote intact','subtitle':'T01 · one mask','selected':True},
           {'id':'r1','frame':2,'x':258,'y':54,'title':'Shell + cover + cells','subtitle':'T01–T04 · selected','selected':True},
           {'id':'ra1','frame':2,'x':258,'y':204,'title':'Keep as one remote','subtitle':'alternative interpretation','selected':False},
           {'id':'r2','frame':4,'x':512,'y':54,'title':'Cells removed','subtitle':'cover stays separate','selected':True},
           {'id':'r3','frame':6,'x':760,'y':54,'title':'Remote reassembled','subtitle':'T05 · one mask','selected':True},
           {'id':'ra2','frame':6,'x':760,'y':204,'title':'Leave parts apart','subtitle':'alternative outcome','selected':False}]
    edges=[{'from':'r0','to':'r1','label':'split proposal','type':'accepted','frame':1},{'from':'r0','to':'ra1','label':'alternative','type':'alternative','frame':1},{'from':'r1','to':'r2','label':'remove cells','type':'accepted','frame':4},{'from':'r2','to':'r3','label':'merge proposal','type':'accepted','frame':6},{'from':'r2','to':'ra2','label':'alternative','type':'alternative','frame':6}]
    return _case('remote','TV remote','Battery-cover and AAA-cell sequence · illustrative component masks, not detected parts.','remote',states,_graph(nodes,edges))


def _usb_case():
    def assembled(): return {'id':'U03','label':'USB drive · assembled','color_role':'whole','shape':{'kind':'roundrect','x':48,'y':58,'w':128,'h':43}}
    def body(): return {'id':'U01','label':'USB body + connector','color_role':'body','shape':{'kind':'roundrect','x':82,'y':58,'w':94,'h':43}}
    def cap(x=48,y=63): return {'id':'U02','label':'Protective cap','color_role':'cap','shape':{'kind':'roundrect','x':x,'y':y,'w':34,'h':33}}
    def connector(): return None
    states=[
      {'title':'Drive assembled','description':'The synthetic USB drive begins as one connected object mask.','motion':'track','objects':[assembled()]},
      {'title':'Cap pulls away','description':'The cap becomes a separate component while the drive body and connector remain linked.','motion':'split','objects':[body(),cap(48,61)]},
      {'title':'Connector exposed','description':'The protective cap is off; the metal connector is visible at the other end.','motion':'track','objects':[body(),cap(48,61)]},
      {'title':'Cap moved aside','description':'The shell, connector, and cap are shown as three explanatory components.','motion':'track','objects':[body(),cap(32,115)]},
      {'title':'Cap stays separate','description':'Alternative paths can keep the cap independent or pair it with the drive.','motion':'candidate','objects':[body(),cap(32,115)]},
      {'title':'Cap approaches','description':'The cap moves back toward the shell; identity is still a proposal.','motion':'candidate','objects':[body(),cap(67,76)]},
      {'title':'Cap reconnects','description':'The protective cap and body overlap in the generated mask.','motion':'merge','objects':[assembled()]},
      {'title':'Drive reassembled','description':'The final state is one illustrative USB-drive mask.','motion':'track','objects':[assembled()]},
    ]
    nodes=[{'id':'u0','frame':0,'x':24,'y':108,'title':'USB assembled','subtitle':'U01 · one mask','selected':True},
           {'id':'u1','frame':2,'x':258,'y':54,'title':'Body + cap','subtitle':'U01 + U02','selected':True},
           {'id':'ua1','frame':2,'x':258,'y':204,'title':'Keep one device','subtitle':'alternative interpretation','selected':False},
           {'id':'u2','frame':4,'x':512,'y':54,'title':'Cap separate','subtitle':'USB parts visible','selected':True},
           {'id':'u3','frame':6,'x':760,'y':54,'title':'Drive reassembled','subtitle':'one connected mask','selected':True},
           {'id':'ua2','frame':6,'x':760,'y':204,'title':'Keep cap apart','subtitle':'alternative outcome','selected':False}]
    edges=[{'from':'u0','to':'u1','label':'split proposal','type':'accepted','frame':1},{'from':'u0','to':'ua1','label':'alternative','type':'alternative','frame':1},{'from':'u1','to':'u2','label':'cap stays separate','type':'accepted','frame':4},{'from':'u2','to':'u3','label':'merge proposal','type':'accepted','frame':6},{'from':'u2','to':'ua2','label':'alternative','type':'alternative','frame':6}]
    return _case('usb','USB flash drive','Cap, body, and connector sequence · illustrative component masks, not detected parts.','usb',states,_graph(nodes,edges))


def build_catalog():
    mug=build_demo(); mug.update(id='mug',title='Travel mug',description='Lid split and reassembly · generated synthetic scene.',scene='mug')
    return {'scenarios':[mug,_remote_case(),_usb_case()]}
