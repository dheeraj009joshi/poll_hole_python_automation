import csv
import json
from selenium import webdriver
import time
import cv2
from matplotlib.contour import QuadContourSet
from selenium import webdriver
import time
# from functions import grt_question_image
from config import ACCESS_KEY, ACCESS_TOKEN, SECRET_KEY, UP_POLL_URL
from PIL import Image
from botocore.exceptions import NoCredentialsError
import random
import urllib.request  
import boto3
import ssl
import requests as r
import requests as re
from tkinter import filedialog as fd
from config import ACCESS_TOKEN, UP_POLL_URL
from functions import filename_person, get_og_image, taking_random_output_total_vote,upload_og_image_to_aws,grt_question_image_from_og_image, upload_question_image_to_aws

 
    

def create_poll():
    head = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data={
    "creater_id":Creator_id,
    "question":Question,
    "question_image":Question_image,
    "tags": Tags,
    "question_type":int(Question_type),
    "status":Status,
    "total_vote": Total_vote,
    "likes_count": Likes_count,
    "dislikes_count": Dislikes_count,
    "answers":[
        {
            "text":"Yes",
            "vote_count":Answer_1__vote_count
        },
        {
            "text":"No",
            "vote_count":Answer_2__vote_count
        },
         {
            "text":"I don't know",
            "vote_count": Answer_3__vote_count
        }
    ],
    "metaData":{
        "meta_title":Question,
        "page_title":Question,
        "meta_description":Question,
        "meta_keywords":Meta_keyword,
        "meta_author":"PollHole",
        "og_title":Question,
        "og_image":Og_image,
        "twitter_card":""
    }
}

    update_poll=re.post(f"{UP_POLL_URL}",json=data,headers=head)
    print(update_poll.status_code)
    print(update_poll.content)
    mm=update_poll.json()
    poll_ids.append(mm["data"]['_id'])




def create_images(url,filename):
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, filename)
filenamee=filename_person() 
poll_ids=[]  
with open(f"{filenamee}",'r',encoding="utf8") as csv_file:
            csv_reader=csv.reader(csv_file)
            next(csv_reader, None)
            for i in csv_reader:
                Creator_id=i[0]
                Question=i[1]
                Tags=i[2].split(",")
                Meta_keyword=i[3]
                Question_type=i[4]
                Status=i[5]
                Total_vote=taking_random_output_total_vote(i[6])
                total_likes_dislikes=int(str(int(Total_vote)*int(taking_random_output_total_vote(i[7]))/100).split(".")[0])
                Likes_count=int(str(total_likes_dislikes*int(taking_random_output_total_vote(i[8]))/100).split(".")[0])
                Dislikes_count=total_likes_dislikes-Likes_count
                Answer_1__vote_count=int(str(Total_vote*int(taking_random_output_total_vote(i[13]))/100).split(".")[0])
                Answer_3__vote_count=int(str(Total_vote*int(taking_random_output_total_vote(i[15]))/100).split(".")[0])
                Answer_2__vote_count=Total_vote-Answer_1__vote_count-Answer_3__vote_count
                get_og_image(i[3])
                grt_question_image_from_og_image()
                image_slug=Question.replace(" ","-").replace("?","").replace(",","").replace(".","")
                og_img=upload_og_image_to_aws("updated_image.jpg",'pollhole-metadata',f"{image_slug}_og_image.jpg")
                Og_image=og_img['url']
                question_img=upload_question_image_to_aws("question_image.jpg",'pollhole-images',f"{image_slug}_question_image.jpg")
                Question_image=question_img['url']
                print(Question_image)
                print(Og_image)
                create_poll()
f= open("poll_ids.py","w") 
f.write(str(poll_ids))

            
            
            