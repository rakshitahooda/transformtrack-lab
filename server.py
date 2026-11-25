from flask import Flask, jsonify, send_from_directory
from pathlib import Path
from core import build_catalog
ROOT=Path(__file__).resolve().parent
app=Flask(__name__,static_folder=str(ROOT/'static'),static_url_path='/static')
@app.get('/')
def home(): return send_from_directory(ROOT,'index.html')
@app.get('/api/demo')
def demo(): return jsonify(build_catalog())
@app.get('/media/pexels-clock-repair.mp4')
def real_footage(): return send_from_directory(ROOT/'media','pexels-clock-repair.mp4',mimetype='video/mp4',conditional=True)
@app.get('/media/transformtrack-demo.mp4')
def demo_video(): return send_from_directory(ROOT/'media','transformtrack-demo.mp4',mimetype='video/mp4',conditional=True)
@app.get('/api/real-footage')
def real_footage_info():
    return jsonify(creator='Tima Miroshnichenko', title='Person Repairing a Clock', source='Pexels', source_url='https://www.pexels.com/video/person-repairing-a-clock-8322341/', license_url='https://www.pexels.com/license/', duration_seconds=14.2, width=2732, height=1440, notes_are_manual=True, computer_vision_runs_on_clip=False)
@app.get('/health')
def health(): return jsonify(status='ok',mode='synthetic-plus-real-footage')
if __name__=='__main__': app.run(host='127.0.0.1',port=8000,debug=False)
