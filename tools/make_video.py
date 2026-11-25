from PIL import Image, ImageDraw, ImageFont
import math, os
W,H=1280,720
OUT='/tmp/tt_frames'; os.makedirs(OUT,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def F(size,b=False,m=False): return ImageFont.truetype(mono if m else bold if b else font,size)
def mix(a,b,t): return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
def rounded(d,box,r,fill,outline=None,w=1): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)
def lantern(d,x,y,assembled=True,alpha=255):
    body=(x-74,y-5,x+74,y+150); cap=(x-58,y-67,x+58,y-32); base=(x-84,y+146,x+84,y+164)
    d.rounded_rectangle(body,18,fill=(111,91,162),outline=(197,183,235),width=3)
    d.rounded_rectangle((x-29,y-34,x+29,y+18),7,fill=(104,84,151),outline=(197,183,235),width=2)
    d.rounded_rectangle((x-49,y+40,x-6,y+122),8,fill=(37,34,52),outline=(194,178,238),width=2)
    d.rounded_rectangle((x+8,y+40,x+51,y+122),8,fill=(37,34,52),outline=(194,178,238),width=2)
    d.ellipse((x-15,y+61,x+15,y+110),fill=(242,193,124))
    d.rounded_rectangle(base,7,fill=(191,161,235),outline=(233,222,251),width=2)
    d.rounded_rectangle(cap,12,fill=(111,194,166),outline=(208,248,230),width=3)
    d.rounded_rectangle((x-43,y-39,x+43,y-24),5,fill=(96,169,143),outline=(208,248,230),width=2)
    if not assembled:
        # redraw cap floating above; opening remains visibly distinct
        d.line((x,y-21,x,y-2),fill=(243,190,121),width=3)
def draw(t):
    img=Image.new('RGB',(W,H),(17,16,25)); d=ImageDraw.Draw(img)
    # soft violet luminous panel background
    d.rectangle((0,0,W,H),fill=(19,18,29))
    for x in range(0,W,48): d.line((x,0,x,H),fill=(29,27,41),width=1)
    for y in range(0,H,48): d.line((0,y,W,y),fill=(29,27,41),width=1)
    rounded(d,(42,30,1238,690),24,(22,21,33),(68,62,91),1)
    d.text((76,57),'TRANSFORMTRACK',font=F(17,True,m=True),fill=(225,218,245));d.text((333,57),'LAB 01',font=F(13,True,m=True),fill=(166,145,207))
    d.text((970,60),'SYNTHETIC SEQUENCE  /  OFFLINE DEMO',font=F(12,m=True),fill=(159,149,177))
    d.line((76,92,1204,92),fill=(60,54,76),width=1)
    d.text((78,118),'WHEN ONE OBJECT',font=F(17,m=True),fill=(183,173,201))
    d.text((78,147),'becomes',font=F(35),fill=(241,236,249));d.text((251,147),'many.',font=F(35,True),fill=(190,163,243))
    d.text((78,202),'Follow identity through assembly and disassembly.',font=F(15),fill=(173,165,190))
    # scene panel
    rounded(d,(76,252,818,588),17,(28,27,41),(64,58,80),1)
    d.text((98,270),'SEQUENCE 01',font=F(11,True,m=True),fill=(166,154,190));d.text((98,291),'Lantern study',font=F(20,True),fill=(237,231,247))
    frame=min(7,int(t*1.05)); split=3<=frame<=5
    progress=(t%1.0)
    x=426+int(13*math.sin(t*2.3)); y=414
    if split:
        # floated part on split / separate states
        lantern(d,x,y,False)
    else:
        lantern(d,x,y,True)
    # overlay rectangle and linkage
    d.rounded_rectangle((x-120,326,x+120,584),18,outline=(167,146,218),width=2)
    if split: d.line((x,y-12,x,y+10),fill=(242,190,126),width=2)
    d.text((96,548),'MASK OVERLAY',font=F(10,m=True),fill=(155,147,172))
    # timeline
    d.text((96,614),'TRANSFORMATION TIMELINE',font=F(10,True,m=True),fill=(161,151,178))
    d.line((99,641,783,641),fill=(91,78,117),width=3)
    for i in range(8):
        xx=100+i*97.5; kind='split' if i==3 else 'merge' if i==6 else ''
        col=(243,190,126) if kind else (165,145,220)
        d.ellipse((xx-6,635,xx+6,647),fill=col)
        if kind: d.text((xx-20,657),kind.upper(),font=F(8,True,m=True),fill=col)
    # right details
    rounded(d,(852,252,1204,409),17,(28,27,41),(64,58,80),1)
    d.text((877,274),'CURRENT STATE',font=F(10,True,m=True),fill=(166,154,190))
    labels=['Assembled','Stable track','Cap starts to move','Split proposal','Parts tracked','Reassembly proposal','Merged state','Identity updated']
    d.text((877,300),labels[frame],font=F(19,True),fill=(236,231,246))
    d.text((877,343),'OBJECT INSTANCES',font=F(9,True,m=True),fill=(144,134,161))
    d.text((877,365),'removable cap  /  lantern body' if split else 'one connected lantern mask',font=F(11,m=True),fill=(204,196,220))
    rounded(d,(852,428,1204,588),17,(28,27,41),(64,58,80),1)
    d.text((877,449),'TRANSFORMATION LOG',font=F(10,True,m=True),fill=(166,154,190))
    d.text((877,477),'1   SPLIT PROPOSAL',font=F(12,True,m=True),fill=(243,190,126))
    d.text((897,500),'one prior mask → two components',font=F(10),fill=(199,190,212))
    d.text((877,531),'2   MERGE PROPOSAL',font=F(12,True,m=True),fill=(139,216,192))
    d.text((897,554),'two tracked parts → one mask',font=F(10),fill=(199,190,212))
    # state graph and footer
    rounded(d,(76,608,1204,665),12,(26,25,38),(64,58,80),1)
    d.text((96,623),'STATE GRAPH',font=F(9,True,m=True),fill=(164,154,182))
    gx=525; gy=635
    for i in range(7):
        xx=gx+i*77; d.line((xx,gy,xx+77,gy),fill=(86,78,104),width=2)
    for i in range(8):
        xx=gx+i*77; c=(243,190,126) if i==3 else (139,216,192) if i==6 else (172,152,228)
        d.ellipse((xx-5,gy-5,xx+5,gy+5),fill=c)
    d.text((76,673),'Synthetic geometry · Python · OpenCV · NumPy · Flask · Canvas',font=F(10,m=True),fill=(141,133,157))
    d.text((1011,673),'NOT REAL-WORLD PERFORMANCE',font=F(9,True,m=True),fill=(177,151,221))
    # small animated scan-line along timeline to make motion purposeful
    scan=100+int((t%7.5)/7.5*680); d.line((scan,631,scan,651),fill=(232,222,255),width=2)
    return img
for frame in range(8*24):
    t=frame/24
    draw(t).save(f'{OUT}/frame_{frame:04d}.png',quality=90)
