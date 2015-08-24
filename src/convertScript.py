# -*- coding: utf-8 -*-
'''
Created on 3.3.2014

@author: Stefan Smihla
'''

import os
import json
import zipfile

F_DIR = '1'
S_DIR = '2'

def convertSamples(inputDir, outputDir):
    """
    Converts samples to more suitable format and prepares them as experimental samples.
    """
    files = [os.path.join(inputDir, f) for f in os.listdir(inputDir)]
    
    for i, zFile in enumerate(files):
        with zipfile.ZipFile(zFile) as zFile:
            for fName in zFile.namelist():
                if fName.split('/')[-1] not in ['feedback.log', '']:
                    fcontent = content = None
                    with zFile.open(fName, 'r') as f:
                        content = json.loads(f.read())
                    with zFile.open('user_biometrics/feedback.log', 'r') as f:
                        fcontent = json.loads(f.read())
                    
                    for key in fcontent:
                        content[key] = fcontent[key]
                    content['username'] = 'user%d' % i
                    saveDir = os.path.join(outputDir, S_DIR) if '2.log' in fName else os.path.join(outputDir, F_DIR);
                        
                    if not os.path.exists(saveDir):
                        os.makedirs(saveDir)
                    
                    with open(os.path.join(saveDir, 'user%s.log' % ("0" + str(i) if i < 10 else str(i))), 'w') as f:
                        f.write(json.dumps(content))