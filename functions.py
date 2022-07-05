import csv
import random
import time
from config import ACCESS_KEY, ACCESS_TOKEN, SECRET_KEY, UP_POLL_URL
import requests as re
from selenium import webdriver
from botocore.exceptions import NoCredentialsError
from PIL import Image
import urllib.request  
from tkinter import filedialog as fd
import boto3
import ssl
import cv2


def upload_og_image_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"https://pollhole-metadata.s3.amazonaws.com/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def upload_question_image_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"https://pollhole-images.s3.amazonaws.com/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
def filename_mcq():
    global filename
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        )
    
def filename_person():
    global filename
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        )
    return filename

def create_images(url,filename):
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, filename)   
 
 
def taking_random_output_total_vote(input)  :
    print(input)
    print()
    print()
    print()
    # try:
    d=(str(input).split("*")[-1].replace("Random","").replace("random","").replace("(","").replace(")","").replace(".","").replace(" - ",",").replace("-",",").replace("%","")).split(",")
    # except:   
    #     d=(str(input).replace("Random","").replace("random","").replace("(","").replace(")","").replace(".","").replace("%","")).split(" – ")
    
    print(d)
    x=d[0]
    y=d[-1]
    
    output=f'{random.randint(int(x),int(y))}'
    return int(output)  


def grt_question_image_from_og_image()  :
    im=cv2.imread("image_demo.jpg", 1)
    height, width, channels = im.shape
    image_aspect_ratio=width/height
    print(image_aspect_ratio)
    im=cv2.resize(im,(1100,int(str(1100/image_aspect_ratio).split(".")[0])))
    cv2.imwrite("question_image.jpg", im)
    
    
def get_og_image(kewords):
    driver=webdriver.Chrome("chromedriver.exe")
    q=kewords
    qq=q.replace(" ","+")
    driver.get(f'https://duckduckgo.com/?q={qq}&t=h_&iax=images&ia=images&iaf=layout%3AWide')
    time.sleep(5)
    img=driver.find_element_by_xpath('//*[@id="zci-images"]/div/div[2]/div/div[1]/div[1]/span/img').get_attribute('src')
    create_images(img,"image_demo.jpg")
    im=cv2.imread("image_demo.jpg", 1)
    height, width, channels = im.shape
    image_aspect_ratio=width/height
    print(image_aspect_ratio)
    im=cv2.resize(im,(1100,int(str(1100/image_aspect_ratio).split(".")[0])))
    cv2.imwrite("updated_image.jpg", im)
    input_image = Image.open("updated_image.jpg")
    watermark = Image.open("logo.png")
    w_w,w_h=watermark.size
    new_image = Image.new('RGB',(1120,int(str(1100/image_aspect_ratio).split(".")[0])+20),(75,217,126))
    new_image.paste(input_image,(10,10))
    new_image.paste(watermark,(1100-w_w,int(str(1100/image_aspect_ratio).split(".")[0])-w_h))
    # new_image.show()
    new_image.save("updated_image.jpg")
