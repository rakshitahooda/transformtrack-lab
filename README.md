# TransformTrack Lab

An original interactive learning prototype about object identity during physical change. It pairs real footage of a watch repair with three separate, synthetic case studies: a travel mug, a TV remote with its cover and AAA cells, and a USB drive with a protective cap.

The watch clip is real, but the app does not run computer vision on it; its chapter notes are manual. Every mask, track ID, overlap score, split/merge proposal, and branching path in the case-study area is generated from hand-authored synthetic shapes. The remote and USB examples teach how a state graph can describe parts; they are not detections from footage. This is not a reproduction of TIPO, a trained real-world tracker, a robotics system, or a VISTA benchmark result.

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

- Open the [captioned demo video](media/transformtrack-demo.mp4). It starts with real watch-repair footage, then shows original illustrative remote-control and USB state diagrams.
- Play the real-world clip and use its manual chapter buttons to jump between moments.
- Choose the mug, TV remote, or USB case study and scrub its eight illustrative frames. The frame view, event evidence, and graph selection stay synchronized.
- Toggle the generated mask overlay. Parts have distinct colors and illustrative track IDs: mug body/lid, remote shell/cover/AAA cells, or USB body/cap.
- At the split and merge frames, inspect shared-pixel counts and per-pair intersection-over-union (IoU).
- Click a node in the graph to jump to its frame. The graph shows an example selected path alongside two alternative hypotheses.

The alternatives are explanatory branches, not competing proposals evaluated by a research model. Track IDs are demonstration labels. Overlap scores are measurements between programmatically generated masks, not semantic confidence or evidence from the real clip.

## Implementation and technology

Python 3.10+, Flask, OpenCV, NumPy, Pillow (for the authored video cards), HTML, CSS, vanilla JavaScript, HTML5 Canvas, SVG, and HTML5 video. Flask serves the real MP4 and the case-study data. The mug study uses OpenCV connected components on authored binary masks; the remote and USB studies provide separate authored component masks. NumPy measures shared pixels, per-mask coverage, and intersection-over-union (IoU). A fixed overlap rule proposes selected splits and merges in the synthetic studies. The browser draws the case illustrations and interactive branching graph; JavaScript synchronizes the frames, evidence, and graph. The real repair clip has only manual chapter navigation.

The included `media/transformtrack-demo.mp4` is an edited walkthrough: licensed watch-repair footage first, followed by original schematic remote/USB slides that are explicitly labeled illustrative. Regenerate it from the included source clip with `python tools/make_video.py`; the authoring script requires `ffmpeg`, Pillow, and a sans-serif font on PATH/system.

## How it differs from the research

The linked paper describes Tracking Instances via Proposals and Overlaps (TIPO): it uses per-object tracker masks, samples components and mask priors, generates and scores candidate states, then applies an MLLM judge for visual validation and semantic labels before updating the state graph and tracker.

This prototype generates synthetic masks from authored geometry, uses connected-component extraction in the mug study, proposes split and merge events from mask overlap, and displays hand-authored explanatory graphs. It does not sample points, decode masks, use a learned tracker, call an MLLM, or evaluate on VISTA. No performance figures from the paper are claimed for this project.

## Tests

Run from the project folder:

```powershell
py -m unittest discover -s tests -v
```

The 12 tests cover generated masks, overlap calculations, mug/remote/USB case content, graph branches, video serving, and the Flask API. They do not evaluate real-video tracking.

## Real-world clip source and license

The app uses the 14-second watch-repair clip [Person Repairing a Clock by Tima Miroshnichenko](https://www.pexels.com/video/person-repairing-a-clock-8322341/). The source listing describes a watch-repair process with hands and tools. The clip was downloaded from Pexels and is included as one component of this interactive app. Pexels’ [license](https://www.pexels.com/license/) says its videos are free to use and modify; attribution is appreciated but not required. The edited demo video credits the creator. This project does not redistribute the clip as a standalone stock asset.

The real-video chapter labels are manual observations, not tracking results. No segmentation, object detection, track IDs, overlap scores, or graph inference are run on the Pexels footage. The mug, remote, and USB case studies are separate deterministic teaching examples with hand-authored component assumptions.

## References

- [Original LinkedIn post](https://lnkd.in/p/gJzuxCi6)
- [Research paper](https://arxiv.org/abs/2611.27398)
- [Official research project page](https://davidegardenal.github.io/tipo-tracking/)
- [VISTA dataset card](https://huggingface.co/datasets/davidegarde/VISTA)

The prototype does not download or redistribute VISTA data.

The repository’s `LICENSE` covers project code. The included Pexels stock footage is not relicensed under MIT; see [`MEDIA_LICENSES.md`](MEDIA_LICENSES.md) for its separate terms and attribution.
