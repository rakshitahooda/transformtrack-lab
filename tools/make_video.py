"""Render an original, captioned TransformTrack walkthrough from the licensed real clip.
Requires ffmpeg on PATH. The source remains credited and the captions state what is manual.
"""
from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "media" / "pexels-clock-repair.mp4"
output = ROOT / "media" / "transformtrack-demo.mp4"
if not source.exists():
    raise SystemExit(f"Missing source clip: {source}")
font_candidates = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "arial.ttf",
]
font_path = next((candidate for candidate in font_candidates if candidate.exists()), None)
if font_path is None:
    raise SystemExit("Could not find DejaVu Sans or Windows Arial font")
font = font_path.as_posix().replace(":", r"\:")
filters = [
    "scale=1280:720:force_original_aspect_ratio=increase",
    "crop=1280:720",
    "drawbox=x=0:y=0:w=iw:h=66:color=0x14121fe8:t=fill",
    "drawbox=x=0:y=594:w=iw:h=126:color=0x14121fee:t=fill",
    f"drawtext=fontfile={font}:text='TRANSFORMTRACK LAB':x=46:y=18:fontsize=24:fontcolor=white",
    f"drawtext=fontfile={font}:text='REAL-WORLD REPAIR FOOTAGE':x=800:y=23:fontsize=15:fontcolor=0xCBB9FF",
    f"drawtext=fontfile={font}:text='Hands work around an exposed watch movement':x=46:y=615:fontsize=24:fontcolor=white:enable='between(t,0,6.99)'",
    f"drawtext=fontfile={font}:text='Precision tools handle the watch movement':x=46:y=615:fontsize=24:fontcolor=white:enable='between(t,7,10.99)'",
    f"drawtext=fontfile={font}:text='The movement is lifted away from its case':x=46:y=615:fontsize=24:fontcolor=white:enable='between(t,11,14.2)'",
    f"drawtext=fontfile={font}:text='MANUAL CHAPTER NOTES · NO AUTOMATIC MASKS OR TRACKS ON THIS CLIP':x=46:y=660:fontsize=13:fontcolor=0xE8C28E",
    f"drawtext=fontfile={font}:text='Footage / Tima Miroshnichenko / Pexels · edited under the Pexels License':x=46:y=688:fontsize=12:fontcolor=0xD2CDD8",
]
subprocess.run([
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
    "-vf", ",".join(filters), "-an", "-c:v", "libx264", "-preset", "medium",
    "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)
], check=True)
print(f"Rendered {output}")
