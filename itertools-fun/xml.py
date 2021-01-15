import os
from xml.etree import ElementTree

file_name = 'Example.xml'
full_file = os.path.abspath(os.path.join('data', file_name))
print(full_file)

dom = ElementTree.parse(file_name)
states = dom.findall('state')
names = []
for x in states:
    names.append((x.attrib.get('name')))


print(" ".join(names))
first = states[0].attrib.get('name')
print(first)
accept = states[1].attrib.get('name')
print(accept)