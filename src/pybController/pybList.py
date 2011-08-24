from PySide.QtCore import *
from PySide.QtGui import *

class pybList():
    
    def getLayout(self):
        return self.layout

    def getWidget(self):
        return self.widget
    
    def getArg(self):
        # TODO
        return self.argument.format(self.labelMap[self.widget.currentText()])
    
    def __init__(self,element):
        # extract information
        labelText = element.find("label").text
        items = element.find("items")
        self.argument = element.find("arg").text
        self.labelMap = {} # stores (label,arg) pairs
    
        # create layout
        self.layout = QHBoxLayout()
        self.widget = QComboBox()
        
        label = QLabel(labelText)
        
        # configure
        
        for i in items: # extracts label,arg pairs, and stores it
            subLabelText = i.find("label").text
            subArg = i.find("arg").text
            self.labelMap[subLabelText] = subArg
            self.widget.addItem(subLabelText)
            
        self.layout.addWidget(label)
        self.layout.addWidget(self.widget)