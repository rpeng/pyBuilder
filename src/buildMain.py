import sys

from PySide.QtCore import *
from PySide.QtGui import *

from pyBuilderQueueWidget import pyBuilderQueueWidget
from pyBuilderMainWidget import pyBuilderMainWidget

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
        self.mainWidget = pyBuilderMainWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        self.setWindowTitle(self.mainWidget.widgets.defaults["project"])
        
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