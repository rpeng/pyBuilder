import sys

from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element as EE

from PySide.QtCore import *
from PySide.QtGui import *

    
class fmoXmlLayoutGenerator():
    
    def handleLineEditElement(self,element):
        # extract details
        labelText = element.find("label").text
        defaultText = element.find("default").text
        # create layout
        hbox = QHBoxLayout()
        tedit = QLineEdit()
        label = QLabel()
        # configure
        label.setText(labelText)
        tedit.setText(defaultText)
        hbox.addWidget(label)
        hbox.addWidget(tedit)
        
        self._layout.addLayout(hbox)
    
    def handleCheckboxElement(self,element):
        # extract our details
        labelText = element.find("label").text
        # create layout
        hbox = QHBoxLayout()
        cbox = QCheckBox()
        label = QLabel()
        # configure
        label.setText(labelText)
        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addWidget(cbox)
        
        
        self._layout.addLayout(hbox)
    
    def __init__(self,_file,_layoutReference):
        self._layout = _layoutReference # a QVBoxLayout!
        layoutTree = ET(file=_file)
        for element in layoutTree.iter():
            if element.tag == "checkbox":
                self.handleCheckboxElement(element)
            elif element.tag == "lineedit":
                self.handleLineEditElement(element)
            
class pyBuilderMainWindow(QWidget):

    def __init__(self, parent=None):
        super(pyBuilderMainWindow,self).__init__(parent)
        # Set up Layouts
        self.mainLayout = QVBoxLayout()
        self.weelabel = QTextEdit()
        self.generator = fmoXmlLayoutGenerator("descriptor.xml",self.mainLayout)
        self.setWindowTitle("Hello World")
        self.setLayout(self.mainLayout)
        self.setFixedSize(self.sizeHint())

app = QApplication(sys.argv)
pymain = pyBuilderMainWindow()
pymain.show()
app.exec_()
sys.exit()