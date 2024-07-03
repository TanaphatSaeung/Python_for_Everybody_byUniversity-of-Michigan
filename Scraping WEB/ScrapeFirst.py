import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import urllib.request, urllib.parse, urllib.error

url = 'https://author-ide.skills.network/render?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZF9pbnN0cnVjdGlvbnNfdXJsIjoiaHR0cHM6Ly9jZi1jb3Vyc2VzLWRhdGEuczMudXMuY2xvdWQtb2JqZWN0LXN0b3JhZ2UuYXBwZG9tYWluLmNsb3VkL0lCTVNraWxsc05ldHdvcmstUFkwMjI0RU4tQ291cnNlcmEvbGFicy9yZWFkaW5nL20xL0NoZWF0c2hlZXQubWQiLCJ0b29sX3R5cGUiOiJpbnN0cnVjdGlvbmFsLWxhYiIsImFkbWluIjpmYWxzZSwiaWF0IjoxNzExNTYyOTgxfQ.ZUVLmGnurE3PzY7tkjGqhUXoNg0FkKjiLRuY9en2PI4'
table_attribs = ['Package/Method','Description','Code Example']

def extract_data(url, table_attribs):
    df = pd.DataFrame(columns=table_attribs)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('text')
    print(soup)

extract_data(url, table_attribs)
