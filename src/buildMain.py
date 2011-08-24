import sys
import os
import shutil
import subprocess as sub

from PySide.QtCore import *
from PySide.QtGui import *

from pybController.pybMain import pybWidgets

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

class pyBuilderQueueWidget(QWidget):
    """
        This widget consists of a build queue list (top) and command line outlet (bottom)
    """
    
    @Slot(str)
    def enqueue(self,arg):
        buildListObject = QListWidgetItem(arg)
        self.builderThread.enqueue(buildListObject)
        self.listWidget.addItem(buildListObject)
    
    @Slot()
    def buildFinished(self):
        self.listWidget.takeItem(0)
    
    @Slot(str)
    def updateOutput(self,arg):
        if arg.lower().find("failed") != -1:
            self.textWidget.append("<font color=red>"+arg+"</font>")
        elif arg.lower().find("success") != -1:
            self.textWidget.append("<font color=green>"+arg+"</font>")
        else:
            self.textWidget.append(arg)
    
    def closeEvent(self, event):
        self.builderThread.stopTask = True
        self.builderThread.exit()
        self.builderThread.wait()
        QWidget.closeEvent(self, event)
    
    def eventFilter(self,obj,event):
        if event.type() == QEvent.ContextMenu:
            menu = QMenu(self)
            action = QAction("Remove",self)
            menu.addAction(action)
            menu.exec_(event.globalPos())
            return False
        return QWidget.eventFilter(self,obj,event)
    
    
    def __init__(self):
        QWidget.__init__(self)
        
        self.builderThread = pyBuilderThread()
        
        self.buildLabel = QLabel("Build Queue")
        self.cmdLabel = QLabel("Command output")
        self.widgetLayout = QVBoxLayout()
        self.listWidget=QListWidget()
        self.textWidget=QTextBrowser()
        
        self.widgetLayout.addWidget(self.buildLabel)
        self.widgetLayout.addWidget(self.listWidget,stretch=1)
        self.widgetLayout.addWidget(self.cmdLabel)
        self.widgetLayout.addWidget(self.textWidget,stretch=3)
        
        self.setLayout(self.widgetLayout)
        self.installEventFilter(self)
        self.listWidget.setSelectionMode(QAbstractItemView.ContiguousSelection)
        
        # conections
        self.builderThread.buildComplete.connect(self.buildFinished)
        self.builderThread.standardOutput.connect(self.updateOutput)
        self.builderThread.start()
    

class pyBuilderMainWidget(QWidget):
    
    buildSignal = Signal(str)
    
    @Slot()
    def build(self):
        args = []
        for i in self.widgets.wList:
            if i.getArg():
                args.append(i.getArg())
        argstr = "ant "+" ".join(args)
        print "Called: "+argstr
        self.buildSignal.emit(argstr)
        
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
        # Set up main layouts
        self.mainLayout = QVBoxLayout()
        self.bottom = QHBoxLayout()
        self.setWindowTitle("Cineplex")
        self.widgets = pybWidgets()
        
        # Set up fmoxml widgets
        self.widgets.generateLayout("descriptor.xml",self.mainLayout)
        self.setLayout(self.mainLayout)
        
        # Set up footer buttons
        self.buildButton = QPushButton("Build")
        self.cancelButton = QPushButton("Close")
        self.buildButton.clicked.connect(self.build)

        self.bottom.addWidget(self.buildButton)
        self.bottom.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.bottom)
        self.mainLayout.addStretch()
        
        # Set up sizing
        self.setMinimumWidth(self.sizeHint().width()+30)
        #self.setFixedHeight(self.sizeHint().height())
        #self.setFixedSize(self.sizeHint())

class pyBuilderMainWindow(QMainWindow):
    
    def readSettings(self):
        settings = QSettings("Fivemobile","PyBuilder")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))
    
    def closeEvent(self,event):
        settings = QSettings("Fivemobile","PyBuilder")
        settings.setValue("geometry",self.saveGeometry())
        settings.setValue("windowState",self.saveState())
        self.mainWidget.closeEvent(event)
        self.buildWidget.closeEvent(event)
        QMainWindow.closeEvent(self,event)
    
    def __init__(self,parent=None):
        QMainWindow.__init__(self)

        self.buildWidget = pyBuilderQueueWidget()
        self.mainWidget = pyBuilderMainWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.dockWidget = QDockWidget("Build Area",self)
        self.dockWidget.setObjectName("BuildDock")
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dockWidget.setWidget(self.buildWidget)
        self.dockWidget.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.dockWidget.setMinimumSize(self.sizeHint())
        self.addDockWidget(Qt.RightDockWidgetArea,self.dockWidget)
        self.setMaximumSize(self.sizeHint().width()+100,self.mainWidget.sizeHint().height()+200)
        # connections
        self.mainWidget.cancelButton.clicked.connect(self.close)
        self.mainWidget.buildSignal.connect(self.buildWidget.enqueue)
        
        # restoring settings
        self.readSettings()
        
    
app = QApplication(sys.argv)
pymain = pyBuilderMainWindow()
pymain.show()
app.exec_()
sys.exit()