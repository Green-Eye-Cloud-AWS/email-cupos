#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
# import requests
from bs4 import BeautifulSoup

from src.core import zeni, fyo

with open(r'otros\raw', 'rb') as f:
    contents = f.read().decode('utf-8')

message = email.message_from_string(contents)

subject, encoding = email.header.decode_header(message['subject'])[0]
if isinstance(subject, bytes):
    subject = subject.decode(encoding)
print(subject)

if message.is_multipart():
    for part in message.walk():
        if part.get_content_type() != 'text/html':
            continue
        data = part.get_payload(decode=True).decode(encoding=part.get_content_charset())            
        break
else:
    if message.get_content_type() == 'text/html':
        data = message.get_payload(decode=True).decode(encoding=message.get_content_charset())

# with open(r'otros/html.html', 'w') as f:
#     f.write(data)

soup = BeautifulSoup(data, 'html.parser')
if subject == 'ZENI':
    cupos = zeni(soup)
elif subject == 'SYNGENTA':
    cupos = fyo(soup)

for cupo in cupos:
    print(cupo.toJSON())
    #res = requests.post(url='http://localhost:3000/back/cupos/cupos', json=cupo.toJSON())
    #print(res.text)



    