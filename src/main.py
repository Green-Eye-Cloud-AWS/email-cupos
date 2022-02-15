import boto3  # type: ignore
import email
import requests
from bs4 import BeautifulSoup

from core import zeni, fyo


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    data = s3.get_object(Bucket=event['Records'][0]['s3']['bucket']['name'], Key=event['Records'][0]['s3']['object']['key'])
    contents = data['Body'].read().decode('utf-8')

    message = email.message_from_string(contents)

    subject, encoding = email.header.decode_header(message['subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    print(subject)
    
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == 'text/html':
                data = part.get_payload(decode=True).decode(encoding=part.get_content_charset())            
                break
    else:
        if message.get_content_type() == 'text/html':
            data = message.get_payload(decode=True).decode(encoding=message.get_content_charset())

    cupos = None
    soup = BeautifulSoup(data, 'html.parser')
    if subject == 'ZENI':
        cupos = zeni(soup)
    elif subject == 'SYNGENTA':
        cupos = fyo(soup)

    if cupos is not None:
        for cupo in cupos:
            print(cupo.toJSON())
            res = requests.post(url='https://greeneye.herokuapp.com/back/cupos/cupos', json=cupo.toJSON())
            print(res.text)
