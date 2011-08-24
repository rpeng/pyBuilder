from PySide.QtCore import *
from PySide.QtGui import *

from pybBaseWidget import pybBaseWidget

class pybList(pybBaseWidget):
    
    def getArg(self): # needs to override this
        # TODO
        argList = []
        formattedList = []
        
        self.listargs = self.labelMap[self.widget.currentText()]["args"]
        self.listexecute = self.labelMap[self.widget.currentText()]["execs"]
        
        for i in self.listargs:
            formattedList.append(self.args[0].format(i))
        
        argList.append((self.ARG_APPEND,formattedList))

        argList.append((self.ARG_EXEC,self.listexecute))
        
        return argList
    
    def __init__(self,element):
        pybBaseWidget.__init__(self, element)
        # extract information
        items = element.find("items")
        self.labelMap = {} # stores (label,arg) pairs
    
        # create layout
        self.layout = QHBoxLayout()
        self.widget = QComboBox()
        
        label = QLabel(self.label)
        
        # configure
        
        for i in items: # extracts label,arg pairs, and stores it
            subLabelText = i.find("label").text
            subArgs = [j.text for j in i.findall("arg")]
            subExecs = [j.text for j in i.findall("exec")]
            self.labelMap[subLabelText] = {}
            
            self.labelMap[subLabelText]["args"] = subArgs
            self.labelMap[subLabelText]["execs"] = subExecs
            
            self.widget.addItem(subLabelText)
            
        self.layout.addWidget(label)
        self.layout.addWidget(self.widget)