# TransformTrack Lab

An original interactive learning prototype about object identity during physical change. It now opens with real footage of hands repairing a watch, followed by a separate synthetic travel-mug study with generated masks, pixel-overlap evidence, and an explorable branching state graph.

The watch clip is real, but this app does not run computer vision on it. The chapter notes are manually written. All measured mask metrics, track IDs, split/merge proposals, and graph states belong only to the synthetic mug sequence. This is not a reproduction of TIPO, a real-world tracker, a robotics system, or a VISTA benchmark result.

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

- Open the [captioned 14-second demo video](media/transformtrack-demo.mp4).
- Play the real-world clip and use its manual chapter buttons to jump between moments.
- Play or scrub eight synthetic frames. The frame view, event evidence and graph selection stay synchronized.
- Toggle the generated mask overlay. The mug body and lid have distinct colors and illustrative track IDs.
- At the split and merge frames, inspect shared-pixel counts and per-pair intersection-over-union (IoU).
- Click a node in the graph to jump to its frame. The graph shows an example selected path alongside two alternative hypotheses.

The alternatives are explanatory branches, not competing proposals evaluated by a research model. Track IDs are demonstration labels. The merge score is a mask-overlap measure, not semantic confidence.

## Implementation and technology

Python 3.10+, Flask, OpenCV, NumPy, HTML5 video, HTML, CSS, vanilla JavaScript, HTML5 Canvas, and SVG. Flask serves the real MP4 and generated scene data. OpenCV extracts connected components from the synthetic binary masks. NumPy measures shared pixels, per-mask coverage, and intersection-over-union (IoU). A fixed overlap threshold proposes splits and merges only for that generated sequence. The browser draws the synchronized synthetic scene and interactive graph; JavaScript provides playback and chapter navigation for the real clip.

The included `media/transformtrack-demo.mp4` is an edited, captioned walkthrough of the real watch-repair footage. Regenerate it from the included source clip with `python tools/make_video.py`; the script requires `ffmpeg` on PATH.

## How it differs from the research

The linked paper describes Tracking Instances via Proposals and Overlaps (TIPO): it uses per-object tracker masks, samples components and mask priors, generates and scores candidate states, then applies an MLLM judge for visual validation and semantic labels before updating the state graph and tracker.

This prototype only generates binary synthetic shapes, extracts connected components, proposes split and merge events using simple mask overlap, and displays a hand-authored explanatory graph. It does not sample points, decode masks, use a learned tracker, call an MLLM, or evaluate on VISTA. No performance figures from the paper are claimed for this project.

## Tests

Run from the project folder:

```powershell
py -m unittest discover -s tests -v
```

The tests cover generated masks, split and merge overlap calculations, track labels, graph branches, and the Flask API. They do not evaluate real video tracking.

## Real-world clip source and license

The app uses the 14-second watch-repair clip [Person Repairing a Clock by Tima Miroshnichenko](https://www.pexels.com/video/person-repairing-a-clock-8322341/). The source listing describes a watch-repair process with hands and tools. The clip was downloaded from Pexels and is included as one component of this interactive app. Pexels’ [license](https://www.pexels.com/license/) says its videos are free to use and modify; attribution is appreciated but not required. The edited demo video credits the creator. This project does not redistribute the clip as a standalone stock asset.

The real-video chapter labels are manual observations, not tracking results. No segmentation, object detection, track IDs, overlap scores, or graph inference are run on the Pexels footage. The synthetic sequence below remains a separate, deterministic teaching example.

## References

- [Original LinkedIn post](https://lnkd.in/p/gJzuxCi6)
- [Research paper](https://arxiv.org/abs/2611.27398)
- [Official research project page](https://davidegardenal.github.io/tipo-tracking/)
- [VISTA dataset card](https://huggingface.co/datasets/davidegarde/VISTA)

The prototype does not download or redistribute VISTA data.

The repository’s `LICENSE` covers project code. The included Pexels stock footage is not relicensed under MIT; see [`MEDIA_LICENSES.md`](MEDIA_LICENSES.md) for its separate terms and attribution.
