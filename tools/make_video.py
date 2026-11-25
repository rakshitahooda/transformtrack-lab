"""Build the original real-footage + illustrative-case walkthrough.
Requires ffmpeg and Pillow. The watch footage remains credited and is never presented as tracked.
"""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "media" / "pexels-clock-repair.mp4"
OUTPUT = ROOT / "media" / "transformtrack-demo.mp4"
FONT_CANDIDATES = [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'), Path('C:/Windows/Fonts/arial.ttf')]
BOLD_CANDIDATES = [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'), Path('C:/Windows/Fonts/arialbd.ttf')]
FONT = next((p for p in FONT_CANDIDATES if p.exists()), FONT_CANDIDATES[0])
BOLD = next((p for p in BOLD_CANDIDATES if p.exists()), BOLD_CANDIDATES[0])
if not SOURCE.exists(): raise SystemExit(f'Missing source clip: {SOURCE}')
if not FONT.exists() or not BOLD.exists(): raise SystemExit('Install DejaVu Sans or Arial fonts and update FONT/BOLD if needed')

def f(size, bold=False): return ImageFont.truetype(str(BOLD if bold else FONT), size)

def arrow(draw, start, end, fill, width=5):
    draw.line([start,end], fill=fill, width=width)
    import math
    a=math.atan2(end[1]-start[1],end[0]-start[0]); L=15
    p1=(end[0]-L*math.cos(a-.48),end[1]-L*math.sin(a-.48))
    p2=(end[0]-L*math.cos(a+.48),end[1]-L*math.sin(a+.48))
    draw.polygon([end,p1,p2],fill=fill)

def card(case):
    im=Image.new('RGB',(1280,720),'#f5f3f7'); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1280,12),fill='#6754a3')
    d.text((58,45),'TRANSFORMTRACK LAB  /  CASE STUDY',font=f(18,True),fill='#65549b')
    if case=='remote':
        d.text((58,93),'A remote control comes apart',font=f(39,True),fill='#20232a')
        d.text((60,150),'Hand-authored parts: remote shell · battery cover · two AAA cells',font=f(19),fill='#5d626b')
        # Original schematic, not source footage.
        d.rounded_rectangle((75,250,300,545),radius=42,fill='#28313a',outline='#11181e',width=6)
        d.ellipse((158,279,216,337),fill='#b54e49')
        for row in range(3):
            for col in range(3): d.ellipse((117+col*54,360+row*50,151+col*54,394+row*50),fill=['#a4b0b4','#89979c','#aa554e'][(row+col)%3])
        d.rounded_rectangle((360,285,490,490),radius=22,fill='#73979a',outline='#45656c',width=5)
        d.text((355,510),'BATTERY COVER',font=f(15,True),fill='#45656c')
        for x,y,label in [(535,310,'AAA A'),(595,310,'AAA B')]:
            d.rounded_rectangle((x,y,x+40,y+148),radius=18,fill='#e0b45f',outline='#936b2f',width=4)
            d.rectangle((x+12,y+8,x+28,y+15),fill='#f4e4bc')
            d.text((x-3,y+164),label,font=f(14,True),fill='#72552c')
        d.text((78,595),'Component masks are illustrative; no real-video detection is claimed.',font=f(16),fill='#727781')
        nodes=[((810,260,970,326),'REMOTE','T01 · one mask'),((1035,205,1210,271),'COVER OFF','T01 + T02'),((1035,358,1210,424),'KEEP CLOSED','alternative'),((1035,505,1210,571),'CELLS OUT','T03 + T04')]
        edges=[((970,293),(1035,238),'#6754a3'),((970,293),(1035,391),'#96909d'),((1122,271),(1122,505),'#6754a3')]
        footer='SELECTED: OPEN → REMOVE CELLS     ·     ALTERNATIVE: KEEP CLOSED'
    else:
        d.text((58,93),'A USB drive separates into parts',font=f(39,True),fill='#20232a')
        d.text((60,150),'Hand-authored parts: protective cap · drive body · connector',font=f(19),fill='#5d626b')
        d.rounded_rectangle((100,318,282,430),radius=34,fill='#547186',outline='#283e50',width=6)
        d.rectangle((282,345,380,403),fill='#c4ced0',outline='#647c84',width=5)
        d.rounded_rectangle((410,330,505,418),radius=22,fill='#bd7595',outline='#74415b',width=5)
        d.text((100,465),'BODY + CONNECTOR',font=f(15,True),fill='#435e70')
        d.text((416,445),'CAP',font=f(15,True),fill='#74415b')
        d.text((62,595),'Illustrative masks and branches; not inferred from footage.',font=f(16),fill='#727781')
        nodes=[((810,260,970,326),'USB DRIVE','U01 · assembled'),((1035,205,1210,271),'CAP OFF','U01 + U02'),((1035,358,1210,424),'KEEP WHOLE','alternative'),((1035,505,1210,571),'CAP REPLACED','one mask')]
        edges=[((970,293),(1035,238),'#6754a3'),((970,293),(1035,391),'#96909d'),((1122,271),(1122,505),'#6754a3')]
        footer='SELECTED: CAP OFF → REATTACH     ·     ALTERNATIVE: KEEP DEVICE WHOLE'
    for (box,title,sub) in nodes:
        alt='alternative' in sub
        d.rounded_rectangle(box,radius=15,fill='#f1eef7' if not alt else '#f5f3f7',outline='#a18fc9' if not alt else '#aaa4b0',width=3)
        d.ellipse((box[0]+15,box[1]+14,box[0]+29,box[1]+28),fill='#8a72bf' if not alt else '#aaa4b0')
        d.text((box[0]+40,box[1]+10),title,font=f(16,True),fill='#302b39')
        d.text((box[0]+16,box[1]+40),sub,font=f(12),fill='#6b6473')
    for a,b,c in edges: arrow(d,a,b,c,5)
    d.rectangle((0,655,1280,720),fill='#24232a')
    d.text((58,678),footer,font=f(16,True),fill='#f2edf8')
    d.text((58,704),'SYNTHETIC / HAND-AUTHORED EXAMPLE · NO MODEL-RANKED BRANCHES',font=f(11),fill='#c9c1d1')
    return im

with tempfile.TemporaryDirectory(prefix='transformtrack-video-') as td:
    td=Path(td); remote=td/'remote.png'; usb=td/'usb.png'
    card('remote').save(remote); card('usb').save(usb)
    font=FONT.as_posix().replace(':',r'\:')
    vf=','.join([
      'scale=1280:720:force_original_aspect_ratio=increase','crop=1280:720',
      'drawbox=x=0:y=0:w=iw:h=76:color=0x14121fe8:t=fill',
      'drawbox=x=0:y=550:w=iw:h=170:color=0x14121fee:t=fill',
      f"drawtext=fontfile={font}:text='TRANSFORMTRACK LAB':x=48:y=18:fontsize=25:fontcolor=white",
      f"drawtext=fontfile={font}:text='REAL WATCH-REPAIR FOOTAGE':x=880:y=23:fontsize=15:fontcolor=0xCBB9FF",
      f"drawtext=fontfile={font}:text='Manual chapter notes; no automatic masks or tracks':x=48:y=576:fontsize=22:fontcolor=white",
      f"drawtext=fontfile={font}:text='Tima Miroshnichenko / Pexels · edited under the Pexels License':x=48:y=626:fontsize=15:fontcolor=0xD2CDD8",
      f"drawtext=fontfile={font}:text='NEXT - SYNTHETIC REMOTE + USB COMPONENT EXAMPLES':x=48:y=672:fontsize=14:fontcolor=0xE8C28E",
    ])
    commands=[
      ['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(SOURCE),'-vf',vf,'-t','14.2','-an','-r','30','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(td/'watch.mp4')],
      ['ffmpeg','-y','-hide_banner','-loglevel','error','-loop','1','-i',str(remote),'-t','4.5','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','medium','-crf','22','-movflags','+faststart',str(td/'remote.mp4')],
      ['ffmpeg','-y','-hide_banner','-loglevel','error','-loop','1','-i',str(usb),'-t','4.5','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','medium','-crf','22','-movflags','+faststart',str(td/'usb.mp4')],
    ]
    for cmd in commands: subprocess.run(cmd,check=True)
    listing=td/'concat.txt'
    listing.write_text("file 'watch.mp4'\nfile 'remote.mp4'\nfile 'usb.mp4'\n",encoding='utf-8')
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUTPUT)],check=True)
print(f'Wrote {OUTPUT}')
