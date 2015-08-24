'''
Created on 2.3.2014

@author: Stefan Smihla
'''

import flask
from biosecDataController import BiosecDataController

HOST = '127.0.0.1'
PORT = 8080

app = flask.Flask(__name__)
storage = BiosecDataController()

@app.route("/")
def index():
    """
    Main page without specific funcion.
    """
    return "BiosecLoggerServer is running!"

@app.route("/checkversion")
def checkversion():
    """
    Returns date of new samples.
    """
    return storage.checkVersion()
           
@app.route("/download")
def download():
    """
    Returns all experimental samples encoded in base64 as JSON.
    Checksum and file name is also included.
    """
    return flask.jsonify(storage.getZipFile())

@app.route("/addsamples", methods=['POST'])
def addsamples():
    """
    Adds samples to storage. Returns 1 if all is ok, else returns 0.
    """
    return storage.processData(flask.request.json)

@app.route('/addsample', methods=['POST'])
def addsample():
    """
    Add one sample to storage. All new samples are validated and stored
    to Good_Samples directory or Wrong_Samples directory.
    """
    return storage.addSample(flask.request.json)

@app.route('/downloadnewsamples')
def downloadnewsamples():
    """
    Download stored samples from Good_Samples directory and Wrong_Samples directory.
    """
    return flask.jsonify(storage.downloadSamples())

if __name__ == "__main__":
    app.run(debug=False)