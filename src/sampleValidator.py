'''
Created on 4.3.2014

@author: Stefan Smihla
'''

from hashlib import md5, sha256
from StringIO import StringIO

import zipfile
import os
import json

SIMPLE_PHRASE = 'vcelimed'
COMPLEX_PHRASE = 'l3kvarov@strudla'

def _wrongSample(data, direct):
    """
    Stores wrong sample to directory.
    """
    if not os.path.exists(direct):
        os.makedirs(direct)
    try:
        with open(os.path.join(direct, data['filename']), 'wb') as f:
            f.write(data['data'].decode('base64'))
    except Exception, e:
        print e
    return 0

def _correctSample(data, direct):
    """
    Stores good sample to directory.
    """
    if not os.path.exists(direct):
        os.makedirs(direct)
    with open(os.path.join(direct, data['filename']), 'wb') as f:
        f.write(data['data'].decode('base64'))
    return 1

def _evalPass(data, password):
    """
    Evaluates password in sample.
    """
    data = json.loads(data)
    phrase = sha256(password).hexdigest()
    return True if data['password'] == phrase else False

def _checkSum(data):
    """
    Evaluates checksum in received sample.
    """
    return True if md5(data['data']).hexdigest() == data['checksum'] else False

def _checkFiles(data):
    """
    Evaluates if correct files are included.
    """
    with zipfile.ZipFile(StringIO(data['data'].decode('base64')), 'r') as zFile:
        files = zFile.namelist()
        
    if len(files) == 3 and 'user_biometrics/feedback.log' in files and any('2.log' in f for f in files):
        return True
    else:
        return False
    
def _checkPassword(data):
    """
    Checks password in files in sample.
    """
    with zipfile.ZipFile(StringIO(data['data'].decode('base64')), 'r') as zFile:
        files = sorted(list(set(zFile.namelist()) - set(['user_biometrics/feedback.log'])))
        check = _evalPass(zFile.read(files[0]), SIMPLE_PHRASE) and _evalPass(zFile.read(files[1]), COMPLEX_PHRASE)
    
    return check

def validateSample(data, goodSampleDir, wrongSampleDir):
    """
    Validates password, file count and checksum in samples and stores them into directory.
    """
    if _checkSum(data) and _checkFiles(data) and _checkPassword(data):
        return _correctSample(data, goodSampleDir)
    else:
        return _wrongSample(data, wrongSampleDir)