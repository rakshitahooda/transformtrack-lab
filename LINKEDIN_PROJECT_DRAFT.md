# LinkedIn Projects draft

Title: TransformTrack Lab: Synthetic Assembly and Disassembly Tracker

Description: Built an interactive computer-vision learning prototype for tracking object identity through assembly and disassembly. A Flask API generates a synthetic lantern sequence; OpenCV extracts connected components, and NumPy scores mask intersections, per-mask coverage, and pairwise IoU to propose split and merge events. A responsive Canvas interface connects the frame timeline, event evidence, and state graph. Includes a self-authored demo clip and tests.

Tech stack: Python, Flask, OpenCV, NumPy, JavaScript, HTML5 Canvas, CSS

Skills: Computer Vision, OpenCV, Python, NumPy, Flask, JavaScript

Scope: Synthetic geometry only. This is an original educational prototype inspired by transformation-tracking research, not a reproduction of TIPO, a trained model, real footage, VISTA evaluation, or robotics-performance claim.

References:
- Source LinkedIn post: https://lnkd.in/p/gJzuxCi6
- Paper: https://arxiv.org/abs/2611.27398
- Official project page: https://davidegardenal.github.io/tipo-tracking/
- Dataset card: https://huggingface.co/datasets/davidegarde/VISTA
