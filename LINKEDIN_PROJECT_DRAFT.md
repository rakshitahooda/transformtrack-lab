# LinkedIn Projects draft

Title: TransformTrack Lab: Real-World Repair Walkthrough + Synthetic State-Graph Study

Description: Built an interactive learning prototype about objects changing state during repair or disassembly. It pairs real Pexels watch-repair footage, with manually written scene notes, and a separate synthetic case-study explorer. The explorer includes a travel mug, a TV remote with a battery cover and AAA cells, and a USB drive with a protective cap. Each case has generated component masks, a frame timeline, pixel-overlap evidence, and a branching graph with selected and alternative paths. The project includes a local Flask app, tests, setup instructions, and an original captioned demo video.

Important scope: The app does not detect or track objects in the real watch video. All masks, IDs, overlap values, and graphs are synthetic and based on hand-authored shapes. Alternatives are not model-ranked; there is no trained model, VISTA evaluation, or reported research performance.

Tech stack: Python 3.10+, Flask, OpenCV, NumPy, Pillow (video-card authoring), HTML, CSS, vanilla JavaScript, HTML5 video and Canvas, SVG.

Skills: Python, Flask, OpenCV, NumPy, Computer Vision fundamentals, video UI, interactive data visualization, testing.

Scope and evidence: The Pexels watch clip is real footage by Tima Miroshnichenko. The app does not run object detection, segmentation, tracking, or mask inference on it; its chapters are manual notes. All masks and IoU values come from deterministic hand-authored synthetic mug, remote, and USB examples. Branch alternatives are explanatory, not model-ranked. This is an educational prototype inspired by transformation-tracking research, not an implementation or reproduction of TIPO, a trained tracker, a VISTA evaluation, or a robotics-performance result.

Footage and license: [Person Repairing a Clock by Tima Miroshnichenko on Pexels](https://www.pexels.com/video/person-repairing-a-clock-8322341/). Pexels’ [license](https://www.pexels.com/license/) permits free use and modification; attribution is appreciated but not required. The demo video credits the creator.

Project repository: https://github.com/rakshitahooda/transformtrack-lab

Captioned demo video: https://github.com/rakshitahooda/transformtrack-lab/blob/main/media/transformtrack-demo.mp4

References: [Source LinkedIn post](https://lnkd.in/p/gJzuxCi6) · [Research paper](https://arxiv.org/abs/2611.27398) · [Official research project page](https://davidegardenal.github.io/tipo-tracking/)
