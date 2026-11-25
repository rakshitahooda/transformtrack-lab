from flask import Flask, jsonify, send_from_directory
from pathlib import Path
from core import build_demo
ROOT=Path(__file__).resolve().parent
app=Flask(__name__,static_folder=str(ROOT/'static'),static_url_path='/static')
@app.get('/')
def home(): return send_from_directory(ROOT,'index.html')
@app.get('/api/demo')
def demo(): return jsonify(build_demo())
@app.get('/health')
def health(): return jsonify(status='ok',mode='synthetic')
if __name__=='__main__': app.run(host='127.0.0.1',port=8000,debug=False)
