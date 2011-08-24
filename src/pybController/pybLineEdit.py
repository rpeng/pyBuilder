from PySide.QtCore import *
from PySide.QtGui import *

class pybLineEdit():
    
    def getLayout(self):
        return self.layout

    def getWidget(self):
        return self.widget
    
    def getArg(self):
        # TODO
        return self.argument.format(self.widget.text())
    
    def __init__(self,element):
        # extract information
        labelText = element.find("label").text
        defaultText = element.find("default")
        self.argument = element.find("arg").text
        
        # create layout
        self.layout = QHBoxLayout()
        if defaultText is not None:
            self.widget = QLineEdit(defaultText.text)
        else:
            self.widget = QLineEdit
        label = QLabel(labelText)
        
        # configure
        
        self.layout.addWidget(label)
        self.layout.addStretch()
        self.layout.addWidget(self.widget)