from requests import Session
from bs4 import BeautifulSoup as bs
import os

USERNAME = "WrongfulRuffian"
PASSWORD = "Szi646Feis!5SWH"
TOKEN = "mau0z9AmDOAVTCl9/23kSk4aSDDoEOcfMOnZVMkwBG4ndirSBvCwlWGAEojxteFPc1gDgcqf3P/etizaRxjIxw=="
AUTH_TOKEN = "VZoLShWDDX3nyZ6X21LJCC4W+F1fKq7DAss3ACBDK68stodpFNxEfGTU0rmXx6UNwr8EOU0eq/vcT+ykHLPBZQ=="

import requests

sess = requests.Session()

req = sess.get('https://archiveofourown.org')
soup = bs(req.text, features='html.parser')
authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']

# Log in to AO3
sess.post('https://archiveofourown.org/users/login', params={
    'authenticity_token': authenticity_token,
    'user[login]': USERNAME,
    'user[password]': PASSWORD,
})

if 'Please try again' in req.text:
    print('Error logging in to AO3; is your password correct?')
    raise SystemExit

# Fetch my private reading history
req = sess.get(f'https://archiveofourown.org/users/{USERNAME}/readings')
print(req.text)


