from PySide.QtCore import *
from PySide.QtGui import *

class pybCheckBox():
    
    def getLayout(self):
        return self.layout

    def getWidget(self):
        return self.widget
    
    def getArg(self):
        # TODO
        if self.widget.isChecked():
            return self.argument
        return None
    
    def __init__(self,element):
        # extract our details
        labelText = element.find("label").text
        defaultText = element.find("default")
        self.argument = element.find("arg").text
        # create layout
        self.layout = QHBoxLayout()
        self.widget = QCheckBox()
        label = QLabel(labelText)
        # configure
        self.layout.addWidget(label)
        self.layout.addStretch()
        self.layout.addWidget(self.widget)
        if defaultText is not None and defaultText.text == "true":
            self.widget.setChecked(True)