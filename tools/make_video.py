"""Render an original 8-second TransformTrack Lab visual explainer."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 720
OUT = '/tmp/tt_frames'
os.makedirs(OUT, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def f(size, bold=False, mono=False): return ImageFont.truetype(MONO if mono else BOLD if bold else FONT, size)
def rr(d, box, r, fill, outline=None, width=1): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
def line(d, pts, fill, width=2): d.line(pts, fill=fill, width=width, joint='curve')

# Original vector artwork: a synthetic mug, lid, colored component masks, and a hand-built graph.
def mug_scene(d, frame, mask=True, t=0):
    rr(d, (54, 138, 755, 514), 20, (238, 226, 205), (219, 207, 190), 2)
    # warm tabletop grain, generated rather than copied from the reference
    for y in range(158, 510, 28): line(d, [(70,y),(738,y)], (229,216,195), 1)
    cx, cy = 402, 324
    split = 3 <= frame <= 5
    # mug body and handle
    rr(d, (cx-92,cy-16,cx+82,cy+154), 31, (82,74,93), (53,46,66), 4)
    d.ellipse((cx+53,cy+35,cx+149,cy+132), outline=(77,67,87), width=18)
    d.ellipse((cx+68,cy+48,cx+134,cy+118), fill=(238,226,205))
    # subtle mug highlight
    rr(d,(cx-74,cy+2,cx-54,cy+133),9,(126,111,142))
    # lid separates but remains visibly connected to its old pixels across adjacent frames
    lid_y = cy-62 if split else cy-16
    rr(d,(cx-103,lid_y,cx+95,lid_y+25),8,(114,181,155),(60,133,109),3)
    rr(d,(cx-76,lid_y-21,cx+66,lid_y+2),7,(137,203,176),(60,133,109),2)
    if split:
        rr(d,(cx-13,lid_y-34,cx+13,lid_y-19),5,(88,160,132))
    if mask:
        # translucent component-like outlines with labels; these are generated shapes, not image masks.
        if split:
            d.rounded_rectangle((cx-115,lid_y-38,cx+108,lid_y+37),12,outline=(32,150,132),width=4)
            d.rounded_rectangle((cx-101,cy-28,cx+162,cy+171),35,outline=(217,117,63),width=4)
            rr(d,(cx-100,lid_y-51,cx-14,lid_y-29),8,(28,115,99)); d.text((cx-93,lid_y-48),'T02 LID',font=f(10,True,True),fill=(255,255,255))
            rr(d,(cx-83,cy+178,cx+5,cy+202),8,(154,77,42)); d.text((cx-76,cy+181),'T01 BODY',font=f(10,True,True),fill=(255,255,255))
        else:
            d.rounded_rectangle((cx-108,cy-31,cx+163,cy+172),38,outline=(115,82,191),width=4)
            rr(d,(cx-101,cy+178,cx-17,cy+202),8,(88,60,151)); d.text((cx-95,cy+181),'T01 MUG',font=f(10,True,True),fill=(255,255,255))
    # small moving playhead marker
    d.ellipse((cx+205,cy-118,cx+213,cy-110),fill=(107,78,167))

STATES=['One connected mask','The lid starts to lift','Two pieces: T01 + T02','Two tracks stay stable','The lid moves back','A merge is proposed','One connected mask again','New whole track: T03']
def draw(t):
    im=Image.new('RGB',(W,H),(247,246,250)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,82),fill=(35,28,52))
    d.text((55,27),'TRANSFORMTRACK LAB',font=f(20,True,True),fill=(248,245,255))
    d.text((906,31),'ORIGINAL SYNTHETIC DEMO  /  NOT CAMERA FOOTAGE',font=f(11,True,True),fill=(201,185,231))
    d.text((57,103),'One mug. Two parts. One story.',font=f(29,True),fill=(42,33,61))
    d.text((59,143),'Watch object identity change as a lid is removed, then reattached.',font=f(15),fill=(101,92,113))
    frame=min(7,int(t)); split=3<=frame<=5
    mug_scene(d,frame,True,t)
    # timeline and timecode
    d.text((73,461),'SYNTHETIC FRAME SEQUENCE',font=f(10,True,True),fill=(87,76,103))
    line(d,[(80,482),(728,482)],(178,164,197),4)
    for i in range(8):
        x=81+i*(647/7); color=(35,143,119) if i in (3,6) else (107,78,167)
        d.ellipse((x-7,475,x+7,489),fill=color)
        if i in (3,6): d.text((x-20,494),'SPLIT' if i==3 else 'MERGE',font=f(8,True,True),fill=color)
    playx=80+(647*(t%8)/7)
    d.ellipse((playx-8,473,playx+8,489),outline=(255,255,255),width=3)
    # right state info panels
    rr(d,(779,138,1225,348),18,(255,255,255),(228,223,235),1)
    d.text((806,161),'FRAME STATE',font=f(10,True,True),fill=(112,98,133))
    d.text((806,190),STATES[frame],font=f(19,True),fill=(48,37,69))
    d.text((806,240),'TRACK IDS',font=f(9,True,True),fill=(133,123,146))
    d.text((806,261),'T01 mug body    T02 removable lid' if split else ('T03 reassembled mug' if frame==7 else 'T01 travel mug'),font=f(12,True),fill=(63,53,82))
    d.text((806,301),'Overlap proposes a change; it does not prove meaning.',font=f(11),fill=(106,97,116))
    # evidence card
    rr(d,(779,365,1225,514),18,(255,255,255),(228,223,235),1)
    d.text((806,386),'TRANSITION EVIDENCE',font=f(10,True,True),fill=(112,98,133))
    d.text((806,413),'Split' if frame==3 else 'Merge' if frame==6 else 'No transition proposed',font=f(15,True),fill=(48,37,69))
    d.text((806,444),'Compare shared pixels and IoU across adjacent masks.',font=f(11),fill=(106,97,116))
    d.text((806,476),'Generated geometry · deterministic · educational',font=f(10,True,True),fill=(125,112,145))
    # readable branching graph: selected route plus rejected alternatives
    rr(d,(54,546,1225,681),18,(255,255,255),(228,223,235),1)
    d.text((77,562),'STATE GRAPH',font=f(10,True,True),fill=(112,98,133))
    # baseline and two branch levels
    y=610; xs=[280,450,620,790,960]
    line(d,[(xs[0],y),(xs[1],y),(xs[2],y),(xs[3],y),(xs[4],y)],(107,78,167),4)
    line(d,[(xs[1],y),(xs[1],653),(xs[2],653)],(188,177,204),2)
    line(d,[(xs[3],y),(xs[3],653),(xs[4],653)],(188,177,204),2)
    d.ellipse((xs[2]-7,646,xs[2]+7,660),fill=(255,255,255),outline=(151,139,169),width=2)
    d.ellipse((xs[4]-7,646,xs[4]+7,660),fill=(255,255,255),outline=(151,139,169),width=2)
    labels=[('WHOLE','T01'),('SPLIT','T01 + T02'),('PARTS','two masks'),('MERGE','T03'),('WHOLE','T03')]
    for j,(lab,sub) in enumerate(labels):
        x=xs[j]
        d.ellipse((x-10,y-10,x+10,y+10),fill=(107,78,167) if j not in (1,3) else (35,143,119))
        d.text((x-31,575),lab,font=f(9,True,True),fill=(74,62,94)); d.text((x-42,629),sub,font=f(8,True,True),fill=(118,108,132))
    d.text((564,666),'KEEP ONE MUG · ALT' ,font=f(8,True,True),fill=(139,129,150))
    d.text((904,666),'KEEP PARTS · ALT' ,font=f(8,True,True),fill=(139,129,150))
    d.text((58,690),'Python · Flask · OpenCV · NumPy · JavaScript     Synthetic prototype, not a TIPO reproduction.',font=f(10,True,True),fill=(94,84,111))
    d.text((1090,690),f'{t:04.1f}s',font=f(10,True,True),fill=(94,84,111))
    return im

for n in range(8*24):
    draw(n/24).save(f'{OUT}/frame_{n:04d}.png')
