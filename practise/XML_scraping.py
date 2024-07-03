import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

html = urllib.request.urlopen('http://py4e-data.dr-chuck.net/comments_2019983.xml').read()
stuff = ET.fromstring(html)
lst = stuff.findall('comments/comment')
print(len(lst))
i = []
for item in lst:
    i.append(int(item.find('count').text))
print(sum(i))
