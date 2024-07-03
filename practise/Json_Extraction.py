import urllib.request, urllib.parse, urllib.error
import json

html = urllib.request.urlopen('http://py4e-data.dr-chuck.net/comments_2019984.json').read()
info = json.loads(html)
lst=[]
for i in range(50):
    lst.append(info['comments'][i]['count'])
print(sum(lst))