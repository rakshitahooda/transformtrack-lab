# TransformTrack Lab

An original interactive learning prototype about object identity during assembly and disassembly. Scrub an overhead synthetic travel-mug sequence, toggle generated mask overlays, inspect pixel-overlap evidence, and follow a branching state graph with selected and alternative paths.

This project takes conceptual inspiration from the research linked below. It is not a reproduction of TIPO, a real video tracker, a robotics system, or a VISTA benchmark result. Every scene frame is generated geometry.

## Windows setup

1. Install Python 3.10 or newer and extract this folder.
2. Open PowerShell in `transformtrack-lab`.
3. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run `.venv\Scripts\python.exe` instead of `py` in the commands below.
4. Install the listed dependencies:
   ```powershell
   py -m pip install --upgrade pip
   py -m pip install -r requirements.txt
   ```
5. Start the local web app:
   ```powershell
   py server.py
   ```
6. On the same PC, open http://127.0.0.1:8000. Leave the terminal open while using the demo. Press Ctrl+C to stop it.

If `py` is not recognized, use `python`. The local URL is reachable only on the computer running the server.

## What to explore

- Play or scrub eight synthetic frames. The frame view, event evidence and graph selection stay synchronized.
- Toggle the generated mask overlay. The mug body and lid have distinct colors and illustrative track IDs.
- At the split and merge frames, inspect shared-pixel counts and per-pair intersection-over-union (IoU).
- Click a node in the graph to jump to its frame. The graph shows an example selected path alongside two alternative hypotheses.

The alternatives are explanatory branches, not competing proposals evaluated by a research model. Track IDs are demonstration labels. The merge score is a mask-overlap measure, not semantic confidence.

## Implementation and technology

Python 3.10+, Flask, OpenCV, NumPy, HTML5 Canvas, SVG, vanilla JavaScript and CSS. Flask serves the generated sequence as JSON. OpenCV extracts connected components from binary masks. NumPy calculates shared pixels, per-mask coverage and IoU. A fixed overlap threshold proposes one-to-many splits and many-to-one merges. The browser draws the synchronized synthetic scene and interactive branching graph.

The included original MP4 is a short visual tour of the generated scene. It is not the research authors' video. Regenerate the clip with `python tools/make_video.py` to render PNG frames, then run:

```bash
ffmpeg -framerate 24 -i /tmp/tt_frames/frame_%04d.png -t 8 -c:v libx264 -pix_fmt yuv420p media/transformtrack-demo.mp4
```

## How it differs from the research

The linked paper describes Tracking Instances via Proposals and Overlaps (TIPO): it uses per-object tracker masks, samples components and mask priors, generates and scores candidate states, then applies an MLLM judge for visual validation and semantic labels before updating the state graph and tracker.

This prototype only generates binary synthetic shapes, extracts connected components, proposes split and merge events using simple mask overlap, and displays a hand-authored explanatory graph. It does not sample points, decode masks, use a learned tracker, call an MLLM, or evaluate on VISTA. No performance figures from the paper are claimed for this project.

## Tests

Run from the project folder:

```powershell
py -m unittest discover -s tests -v
```

The tests cover generated masks, split and merge overlap calculations, track labels, graph branches, and the Flask API. They do not evaluate real video tracking.

## References

- [Original LinkedIn post](https://lnkd.in/p/gJzuxCi6)
- [Research paper](https://arxiv.org/abs/2611.27398)
- [Official research project page](https://davidegardenal.github.io/tipo-tracking/)
- [VISTA dataset card](https://huggingface.co/datasets/davidegarde/VISTA)

The prototype does not download or redistribute VISTA data.
