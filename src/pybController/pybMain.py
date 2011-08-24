"""
    Main pyBuilder module
    Contains all of the required classes to make use of pybWidgets
"""
from pybCheckBox import pybCheckBox
from pybLineEdit import pybLineEdit
from pybList import pybList

from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element as EE

class pybWidgets():
    # base class for all pyBuilder Widgets
    
    # static variables
    switch = { # switch to contain the widget classes
              "lineedit":pybLineEdit,
              "checkbox":pybCheckBox,
              "list":pybList
    }
    
    # instance methods
    def generateLayout(self,descriptor,verticalLayout):
        self.wList = [] # contains all of the widgets
        self._layout = verticalLayout
        self._descriptor = descriptor
        self._layoutTree = ET(file=self._descriptor)
        for element in self._layoutTree.iter():
            if element.tag in pybWidgets.switch.keys():
                widget = pybWidgets.switch[element.tag](element)
                verticalLayout.addLayout(widget.getLayout())
                self.wList.append(widget)
        
    def __init__(self):
        pass