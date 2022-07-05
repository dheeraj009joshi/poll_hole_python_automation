import json
from multiprocessing import context
import urllib.request  
import boto3
import ssl
import requests as re
from botocore.exceptions import NoCredentialsError
from PIL import Image
from config import ACCESS_KEY, ACCESS_TOKEN, SECRET_KEY, UP_POLL_URL



def add_images_4(i1,i2,i3,i4,image_slug):
    """i1,i2,i3,i4 are the urls of the images"""
    create_images(i1,"im1.png")
    create_images(i2,"im2.png")
    create_images(i3,"im3.png")
    create_images(i4,"im4.png")
    image1 = Image.open("im1.png")
    image2 = Image.open("im2.png")
    image3 = Image.open("im3.png")
    image4 = Image.open("im4.png")
    new_image = Image.new('RGB',(1200,600) ,(50,205,50))
    size=(590,290)
    image1 = image1.resize(size)
    image2 = image2.resize(size)
    image3 = image3.resize(size)
    image4 = image4.resize(size)
    new_image.paste(image1,(5,5))
    new_image.paste(image2,(592,5))
    new_image.paste(image3,(5,292))
    new_image.paste(image4,(592,292))
    # new_image.paste(vs,(500,250))
    new_image.show()
    new_image.save(image_slug)
    
    
    
def add_images_2(i1,i2,image_slug):
    """i1,i2,i3,i4 are the urls of the images"""
    create_images(i1,"im1.png")
    create_images(i2,"im2.png")
    image1 = Image.open("im1.png")
    image2 = Image.open("im2.png")
    new_image = Image.new('RGB',(1200,600) ,(50,205,50))
    size=(590,588)
    image1 = image1.resize(size)
    image2 = image2.resize(size)
    new_image.paste(image1,(5,5))
    new_image.paste(image2,(605,5))
    # new_image.paste(vs_1,(550,280))
    new_image.show()
    new_image.save(image_slug)
    
    


 
def create_images(url,filename):
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, filename)
    
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False