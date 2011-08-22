from xml.etree.ElementTree import ElementTree as ET

tree = ET(file="descriptor.xml")

for element in tree.getiterator():
    print element.tag