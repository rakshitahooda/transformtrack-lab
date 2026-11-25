# LinkedIn Projects draft

Title: TransformTrack Lab: Real-World Repair Walkthrough + Synthetic State-Graph Study

Description: Built an interactive computer-vision learning prototype that pairs freely licensed real watch-repair footage with a separate, transparent synthetic tracking study. The real clip shows hands working around an exposed watch movement and lifting it from its case; manually written chapter notes make key moments easy to inspect. A separate generated travel-mug sequence demonstrates how connected-component masks, pixel overlap, per-mask coverage, and IoU can suggest split and merge events. An interactive timeline stays in sync with the synthetic scene, evidence panel, and branching state graph. The project includes a local Flask app, tests, setup instructions, and an original captioned demo video.

Tech stack: Python 3.10+, Flask, OpenCV, NumPy, HTML, CSS, vanilla JavaScript, HTML5 video and Canvas, SVG.

Skills: Python, Flask, OpenCV, NumPy, Computer Vision fundamentals, video UI, interactive data visualization, testing.

Scope and evidence: The Pexels watch clip is real footage by Tima Miroshnichenko. The app does not run object detection, segmentation, tracking, or mask inference on that clip; its chapters are manual notes. All measured masks and IoU values come from a deterministic synthetic mug sequence. Its branch alternatives are explanatory, not model-ranked. This is an educational prototype inspired by transformation-tracking research, not an implementation or reproduction of TIPO, a trained tracker, a VISTA evaluation, or a robotics-performance result.

Footage and license: [Person Repairing a Clock by Tima Miroshnichenko on Pexels](https://www.pexels.com/video/person-repairing-a-clock-8322341/). Pexels’ [license](https://www.pexels.com/license/) permits free use and modification; attribution is appreciated but not required. The demo video credits the creator.

Project repository: https://github.com/rakshitahooda/transformtrack-lab

Captioned demo video: https://github.com/rakshitahooda/transformtrack-lab/blob/main/media/transformtrack-demo.mp4

References: [Source LinkedIn post](https://lnkd.in/p/gJzuxCi6) · [Research paper](https://arxiv.org/abs/2611.27398) · [Official research project page](https://davidegardenal.github.io/tipo-tracking/)
