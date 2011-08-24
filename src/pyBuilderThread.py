import subprocess as sub

from PySide.QtCore import *
from PySide.QtGui import *

class pyBuilderThread(QThread):
    """ build worker thread"""
    
    buildComplete = Signal()
    standardOutput = Signal(str)
    
    @Slot(QListWidgetItem)
    def enqueue(self,qitem):
        self.buildList.append(qitem)
    
    @Slot(QListWidgetItem)
    def remove(self,qitem):
        self.buildList.remove(qitem)
        
    def run(self):
        ## Build logic
        while(True):
            if self.stopTask:
                return
            if self.abort:
                if self.processHandle is not None:
                    self.processHandle.kill()
                self.processHandle = None
                self.currentProcess = None
            self.msleep(100) # to not be a hog
            if self.currentProcess is None: # no build in progress
                if len(self.buildList) == 0:
                    pass # nothing to do!
                else:
                    self.currentProcess = self.buildList.pop(0)
            else: # in the middle of a build!
                if self.processHandle is None: # build process has not started!
                    self.processHandle = sub.Popen(self.currentProcess.text(),
                                                   stdout=sub.PIPE,
                                                   stderr=sub.STDOUT,
                                                   shell=True)
                else: # building in progress!
                    line = self.processHandle.stdout.readline()
                    if line != '':
                        self.standardOutput.emit(line)
                    else: # building done!
                        self.buildComplete.emit()
                        self.processHandle = None
                        self.currentProcess = None
                    
    def __init__(self):
        QThread.__init__(self)
        self.abort = False
        self.stopTask = False
        self.buildList = []
        self.currentProcess = None # a qlistwidget item
        self.processHandle = None