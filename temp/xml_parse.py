#!/usr/bin/python
import xml.etree.ElementTree as ET
tree = ET.parse('2007_000027.xml')
root = tree.getroot()

i=0
print "Person bound box (xy_min,xy_max): ((%s,%s),(%s,%s))" % (root[5][4][0].text,root[5][4][1].text,root[5][4][2].text,root[5][4][3].text)

for part in root.iter('part'):
   print "%s bound box: ((%s,%s),(%s,%s))" % (part[0].text,part[1][0].text,part[1][1].text,part[1][2].text,part[1][3].text)