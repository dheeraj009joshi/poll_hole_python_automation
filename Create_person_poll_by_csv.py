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

from functions import filename_person, get_og_image, grt_question_image_from_og_image, taking_random_output_total_vote, upload_og_image_to_aws, upload_question_image_to_aws



filename=filename_person()
def Person_poll_data():
    
    head = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data_create_poll={
        "creater_id":Creator_id,
        "question":Person_name,
        "question_image":Question_image,
        "tags":[{
            "tag_name":Tags

        }],
            "answers":[
        {

            "image":Question_image
        }
        ],
        "status":Status,
        "question_type":int(Question_type),
        "total_vote": Total_vote,
        "likes_count":Likes_count,
        "dislikes_count":Dislikes_count,
        "metaData":{
            "meta_title":Person_name,
            "page_title":Person_name,
            "meta_description":Person_name,
            "meta_keywords":Person_name,
            "meta_author":"Pollhole",
            "og_title":f"{Person_name}'s Approval Rating",
            "og_image":Person_image,
            "twitter_card":""
        }
}
    # print(data_create_poll)
    update_poll=re.post(f"{UP_POLL_URL}",json=data_create_poll,headers=head)
    print(update_poll.status_code)
    print(update_poll.json())

with open(f"{filename}",'r',encoding="utf8") as csv_file:
            csv_reader=csv.reader(csv_file)
            next(csv_reader, None)
            global Creator_id
            global Question
            global Tags
            global Meta_keyword
            global Question_type
            global Status
            global Total_vote
            global Likes_count
            global Dislikes_count
            global Og_image
            global poll_ids
            poll_ids=[]
            for i in csv_reader:
                Creator_id=i[0]
                Person_name=i[1]
                Tags=i[2].split(",")
                Meta_keyword=i[3]
                Question_type=i[4]
                Status=i[5]
                Total_vote=taking_random_output_total_vote(i[6])
                # total_likes_dislikes=int(str(int(Total_vote)*int(taking_random_output_total_vote(i[7]))/100).split(".")[0])
                Likes_count=int(str(Total_vote*int(taking_random_output_total_vote(i[7]))/100).split(".")[0])
                Dislikes_count=Total_vote-Likes_count
                get_og_image(i[3])
                grt_question_image_from_og_image()
                image_slug=Person_name.replace(" ","-").replace("?","")
                og_img=upload_og_image_to_aws("updated_image.jpg",'pollhole-metadata',f"{image_slug}-og-image.jpg")
                question_img=upload_question_image_to_aws("question_image.jpg",'pollhole-images',f"{image_slug}-question-image.jpg")
                Question_image=question_img['url']
                Person_image=og_img['url']
                print(Question_image)
                Person_poll_data()
                
                
            