'''
Created on 2.3.2014

@author: Stefan Smihla
'''

import os, zipfile, time
from dateutil.parser import parse
from hashlib import md5
from StringIO import StringIO

from sampleValidator import validateSample
import convertScript

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DATA_DIR = os.path.join(STORAGE_DIR, 'biosec_data')
PACKED_FILE = os.path.join(STORAGE_DIR, 'biosec_data.zip')
SAMPLES_DIR = os.path.join(STORAGE_DIR, 'samples')
GOOD_SAMPLES_DIR = os.path.join(STORAGE_DIR, 'good_samples')
WRONG_SAMPLES_DIR = os.path.join(STORAGE_DIR, 'wrong_samples')
SAMPLES_PACKED_FILE = os.path.join(STORAGE_DIR, 'new_samples.zip')

class BiosecDataController(object):
    """
    Class handles all requests from server. 
    """
    
    def __init__(self):
        """
        Inits instance of class.
        """
        pass
    
    def processData(self, data):
        """
        Loads samples and converts them to experimental format and prepares zip file.
        Returns 1 if all ok, else returns 0.
        """
        if md5(data['data']).hexdigest() != data['checksum']:
            return str(0)
        
        with zipfile.ZipFile(StringIO(data['data'].decode('base64')), 'r') as zFile:
            for f in zFile.namelist():
                direct = os.path.dirname(f)
                if not os.path.exists(os.path.join(STORAGE_DIR, direct)):
                    os.makedirs(os.path.join(STORAGE_DIR, direct))
                with open(os.path.join(STORAGE_DIR, f), 'wb') as sf:
                    sf.write(zFile.read(f))
            
        self.convertSamples()
        self.createZipFile()
        return str(1)
    
    def createZipFile(self):
        """
        Creates zip file from experimental samples.
        """
        with zipfile.ZipFile(PACKED_FILE, 'w') as zFile:
            [[zFile.write(os.path.join(root, f), os.path.join(root.split(STORAGE_DIR)[-1], f)) for f in files] for root, _, files in os.walk(DATA_DIR)]
        
    def getZipFile(self):
        """
        Returns base64 encoded zip file in JSON format.
        """
        with open(PACKED_FILE, 'rb') as f:
            data = f.read().encode('base64')
            
        return {'filename': os.path.basename(PACKED_FILE), 'data': data, 'checksum': md5(data).hexdigest()}
    
    def checkVersion(self):
        """
        Checks version of samples. Returns their date.
        """
        return str(parse(time.ctime(os.path.getmtime(PACKED_FILE))))
    
    def convertSamples(self):
        """
        Convert samples to experimental format.
        """
        convertScript.convertSamples(SAMPLES_DIR, DATA_DIR)
        return True
    
    def addSample(self, data):
        """
        Adds new sample to storage.
        """
        return str(1) if validateSample(data, GOOD_SAMPLES_DIR, WRONG_SAMPLES_DIR) == 1 else str(0)
    
    def downloadSamples(self):
        """
        Downloads non experimental samples.
        """
        with zipfile.ZipFile(SAMPLES_PACKED_FILE, 'w') as zFile:
            if os.path.exists(GOOD_SAMPLES_DIR): 
                [[zFile.write(os.path.join(root, f), os.path.join(root.split(STORAGE_DIR)[-1], f)) for f in files] for root, _, files in os.walk(GOOD_SAMPLES_DIR)]
            if os.path.exists(WRONG_SAMPLES_DIR):
                [[zFile.write(os.path.join(root, f), os.path.join(root.split(STORAGE_DIR)[-1], f)) for f in files] for root, _, files in os.walk(WRONG_SAMPLES_DIR)]
        
        with open(SAMPLES_PACKED_FILE, 'rb') as f:
            content = f.read().encode('base64')
            filename = os.path.basename(SAMPLES_PACKED_FILE)
            
        return {'filename':filename, 'data': content, 'checksum': md5(content).hexdigest()}