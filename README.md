# TransformTrack Lab

An original local-first interactive prototype for understanding how object identity can change during assembly and disassembly. Follow a synthetic lantern through a split and merge, inspect mask-overlap evidence, and explore its state graph.

This is a teaching prototype inspired by the research below. It does not reproduce TIPO or VISTA benchmark results. The sequence is generated synthetic geometry, not real footage or robotics performance.

## Run on Windows
1. Install Python 3.10+ and extract this folder. Open PowerShell in `transformtrack-lab`.
2. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If activation is blocked, use `.venv\Scripts\python.exe` instead of `py` below.
3. Install dependencies:
   ```powershell
   py -m pip install --upgrade pip
   py -m pip install -r requirements.txt
   ```
4. Start the server:
   ```powershell
   py server.py
   ```
5. On that same PC, open http://127.0.0.1:8000. Keep PowerShell open; stop with Ctrl+C.

If `py` is unavailable, replace it with `python`. The local address works only on the computer running the server.

## Prototype and stack
Python 3.10+, Flask, OpenCV, NumPy, Pillow (for regenerating the included clip), HTML5 Canvas, vanilla JavaScript and CSS. Flask serves a JSON analysis endpoint. OpenCV extracts connected components from generated instance masks; NumPy computes pixel intersections, per-mask coverage and IoU. A pair is linked when it overlaps at least 8% of either mask. One prior mask overlapping multiple current masks proposes a split; multiple prior masks overlapping one current mask propose a merge. Displayed mean pair IoU is an overlap measure, not a calibrated confidence. The UI shows eight sample states and a linked state graph. No model is trained or downloaded.

The included original MP4 is a short visual tour of the synthetic sequence. It is not the source creator's video. Watch it at [media/transformtrack-demo.mp4](media/transformtrack-demo.mp4). Regenerate it by running `python tools/make_video.py` to render PNG frames, then `ffmpeg -framerate 24 -i /tmp/tt_frames/frame_%04d.png -t 8 -c:v libx264 -pix_fmt yuv420p media/transformtrack-demo.mp4`.

## Research pipeline concept and this prototype
The referenced TIPO work describes a broader tracking loop: per-object tracker masks; component extraction with point sampling and mask decoding; candidate assembly or disassembly state proposals; overlap-based scoring and selection; an MLLM judge for semantic validation and labels; then updates to a state graph and tracker. The diagram in the web demo is an original summary of that flow, not a reproduction of the paper figure.

TransformTrack implements only a small synthetic analogy: it generates binary masks, extracts connected components with OpenCV, proposes split or merge events using an overlap threshold and reports mean pairwise IoU, then builds a finite synthetic state graph. It does not sample prompts, decode masks, run an MLLM, maintain a learned tracker, or implement the TIPO method. Its values are educational examples, not benchmark metrics or confidence estimates.

## Tests
```powershell
py -m unittest discover -s tests -v
```
The tests exercise synthetic mask handling and split/merge proposals, not a real video tracker.

## Limits
No camera input, learned segmentation model, MLLM judge, physical robot, real-world trial, VISTA evaluation, or generalization claim. This mask-overlap example is a small educational analogue, not the paper's TIPO implementation. The paper's project page describes its own TIPO pipeline; the dataset card currently says project page, paper and code with evaluation are “Coming Soon”. This project does not download or redistribute VISTA data.

## Attribution
- LinkedIn source post: https://lnkd.in/p/gJzuxCi6
- Paper by Davide Gardenal, Mingxuan Liu, Flavio Vella, Quentin Guimard and Elisa Ricci: https://arxiv.org/abs/2611.27398
- Official research project page: https://davidegardenal.github.io/tipo-tracking/
- VISTA dataset card (CC BY 4.0): https://huggingface.co/datasets/davidegarde/VISTA
