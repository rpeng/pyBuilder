from PySide.QtCore import *
from PySide.QtGui import *

from pybController.pybBaseWidget import pybBaseWidget

class pybLineEdit(pybBaseWidget):
    
    def formatArg(self,arg):
        return arg.format(self.widget.text())
        
    
    def __init__(self,element):
        pybBaseWidget.__init__(self, element)
        # create layout
        self.layout = QHBoxLayout()
        if self.default is not None:
            self.widget = QLineEdit(self.default)
        else:
            self.widget = QLineEdit()
        label = QLabel(self.label)
        
        # configure
        
        self.layout.addWidget(label)
        self.layout.addStretch()
        self.layout.addWidget(self.widget)