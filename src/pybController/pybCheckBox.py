from PySide.QtCore import *
from PySide.QtGui import *

from pybBaseWidget import pybBaseWidget

class pybCheckBox(pybBaseWidget):
    
    def getArg(self):
        if self.widget.isChecked():
            return pybBaseWidget.getArg(self)
        return None
    
    def __init__(self,element):
        pybBaseWidget.__init__(self, element)
        
        # create layout
        self.layout = QHBoxLayout()
        self.widget = QCheckBox()
        label = QLabel(self.label)
        # configure
        self.layout.addWidget(label)
        self.layout.addStretch()
        self.layout.addWidget(self.widget)
        if self.default is not None and self.default == "true":
            self.widget.setChecked(True)