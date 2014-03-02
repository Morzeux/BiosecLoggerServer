'''
Created on 2.3.2014

@author: Morzeux
'''

from flask import Flask
from biosecDataController import BiosecDataController

HOST = '127.0.0.1'
PORT = 8080
DATA_DIR = 'biosec_data'
PACKED_FILE = 'biosec_data.zip'

app = Flask(__name__)
storage = BiosecDataController(DATA_DIR, PACKED_FILE)

@app.route("/")
def index():
    return "BiosecLoggerServer is running!"

@app.route("/checkversion")
def checkversion():
    return storage.checkVersion()
        
    
@app.route("/download")
def download():
    return storage.getZipFile()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)