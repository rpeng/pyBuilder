from PySide.QtCore import *
from PySide.QtGui import *

from pybController.pybMain import pybWidgets
from pybController.pybBaseWidget import pybBaseWidget

class pyBuilderMainWidget(QWidget):
    
    buildSignal = Signal(str)
    
    @Slot()
    def build(self):
        # need better way of queuing up args!
        args = []
        
        callableList = [] # list of callable objects
                        # example [ ["ant","-lib build/lib"] , ["svn","update"] ]
                        
        callableList.append(["ant"])
        
        for i in self.widgets.wList:
            if i.getArg():
                args.extend(i.getArg())
        
        for type,arglist in args:
            if type == pybBaseWidget.ARG_APPEND:
                newList = []
                for prefixes in callableList: # prefixes (list)
                    if prefixes is None:
                        continue
                    for postElement in arglist: # post element (string)
                        tempList = list(prefixes)
                        tempList.append(postElement)
                        newList.append(tempList)
                callableList = newList
            elif type == pybBaseWidget.ARG_EXEC:
                for execString in arglist:
                    self.buildSignal.emit(execString) # execute literal callable string
        
        for i in callableList:
            callstr = " ".join(i)
            print "Called: "+callstr
            self.buildSignal.emit(callstr)
        
        """
        argstr = "ant "+" ".join(args)
        print "Called: "+argstr
        self.buildSignal.emit(argstr)
        """
        
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
        # Set up main layouts
        self.mainLayout = QVBoxLayout()
        self.bottom = QHBoxLayout()
        self.widgets = pybWidgets()
        
        # Set up fmoxml widgets
        self.widgets.generateLayout("descriptor.xml",self.mainLayout)
        self.setWindowTitle(self.widgets.defaults["project"])
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
