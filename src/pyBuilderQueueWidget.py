
from PySide.QtCore import *
from PySide.QtGui import *

from pyBuilderThread import pyBuilderThread

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