import os
import json
import uuid
import boto3

from PIL import Image
from rembg import remove
import warnings

img_width = 200
img_height = 200
dest_bucket = '<your-bucket-name>'
s3_client = boto3.client('s3')

warnings.filterwarnings(action='ignore', message='Could not obtain multiprocessing lock')


def handler(event, context):
    print(event)
    print('start photo conversion')
    
    # getting bucket and object key from event object
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # creating download path and downloading the img object from S3
    object_key = str(uuid.uuid4()) + '-' + key
    img_download_path = '/tmp/{}'.format(object_key)
    
    with open(img_download_path, 'wb') as img_file:
        s3_client.download_fileobj(source_bucket, key, img_file)
    
    removed_bg = '/tmp/hero-{}.png'.format(object_key)

    source_img = Image.open(img_download_path)
    print('starting rembg')
    # use rembg to strip foreground
    output = remove(source_img)
    output.save(removed_bg)
    print('finished rembg')
    
    # uploading img thumbnail to destination bucket
    upload_key = '{}-hero.png'.format(key)
    s3_client.upload_file(removed_bg, dest_bucket, upload_key)
