# LinkedIn Projects draft

Title: TransformTrack Lab: Synthetic Assembly and Disassembly Tracker

Description: Built an interactive computer-vision learning prototype that follows a synthetic travel mug as its lid separates and is reattached. A Flask API serves an eight-frame generated sequence. OpenCV finds connected components in binary masks, while NumPy measures shared pixels, per-mask coverage, and pairwise IoU to propose split and merge transitions. The browser ties a generated, video-like scene to its timeline, colored component labels, measured transition evidence, and an explorable branching state graph with selected and alternative paths. Includes an original generated demo clip and automated tests.

Tech stack: Python, Flask, OpenCV, NumPy, HTML, CSS, JavaScript, HTML5 Canvas, SVG

Skills: Computer Vision, Python, OpenCV, NumPy, Flask, JavaScript, Data Visualization

Scope: The sequence uses deterministic synthetic geometry, not camera video. Track labels are explanatory IDs. Branch alternatives are hand-authored illustrations, not model-ranked hypotheses. This is an original educational prototype inspired by transformation-tracking research, not an implementation or reproduction of TIPO, a trained tracker, VISTA evaluation, or a robotics-performance claim. It does not implement point sampling, mask decoding, learned segmentation, or an MLLM judge.

References:
- Source LinkedIn post: https://lnkd.in/p/gJzuxCi6
- Paper: https://arxiv.org/abs/2611.27398
- Official project page: https://davidegardenal.github.io/tipo-tracking/
- Dataset card: https://huggingface.co/datasets/davidegarde/VISTA
