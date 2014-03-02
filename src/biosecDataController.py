'''
Created on 2.3.2014

@author: Morzeux
'''

import os, zipfile, time

class BiosecDataController(object):
    
    def __init__(self, dataDir, packedData):
        self.dataDir = dataDir
        self.packedData = packedData
        
        self.createZipFile()
         
    
    def createZipFile(self):
        zipf = zipfile.ZipFile(self.packedData, 'w')
        
        for root, dirs, files in os.walk(self.dataDir):
            for f in files:
                zipf.write(os.path.join(root, f))
        
        zipf.close()
        
    def getZipFile(self):
        with open(self.packedData, 'rb') as f:
            data = f.read()
            
        return data.encode('base64')
    
    def checkVersion(self):
        return time.ctime(os.path.getmtime(self.packedData))