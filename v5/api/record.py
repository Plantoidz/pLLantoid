# app.py (using Flask)
from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
  timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  file = request.files['audio']
  filename = f'recordings/{timestamp}_recording.wav'
  file.save(filename)
  with open(filename, 'rb') as f:
    audio_data = f.read()
  response = requests.post('https://remote-api.com/process-audio', data=audio_data)
  return response.text

if __name__ == '__main__':
  app.run()
