import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

start_url = 'http://py4e-data.dr-chuck.net/known_by_Rhienna.html'
current_url = start_url
for _ in range(7):
    html = urllib.request.urlopen(current_url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    current_url = tags[17].get('href')
    name = tags[17].text
    print(current_url,name)
