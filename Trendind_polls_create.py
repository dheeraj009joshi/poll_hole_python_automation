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


def upload_to_aws(local_file, bucket, s3_file):
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
    

def filename_mcq():
    global filename_mcq
    filename_mcq = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        )
def filename_person():
    global filename_person
    filename_person = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        )

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

def grt_question_image()  :
    im=cv2.imread("image_demo.jpg", 1)
    height, width, channels = im.shape
    image_aspect_ratio=width/height
    print(image_aspect_ratio)
    im=cv2.resize(im,(1100,int(str(1100/image_aspect_ratio).split(".")[0])))
    cv2.imwrite("question_image.jpg", im)
    
    
def mcq_poll_data():
   
    head = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data={
    "creater_id":Creator_id,
    "question":Question,
    "tags": Tags,
    "question_type":Question_type,
    "status":Status,
    "total_vote": Total_vote,
    "likes_count": Likes_count,
    "dislikes_count": Dislikes_count,
    "question_image":Question_image,
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

def Person_poll_data():
    
    head = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data_create_poll={
        "creater_id":Creator_id,
        "question":person_name,
        "tags":[{
            "tag_name":Tags

        }],
            "answers":[
        {

            "image":person_image
        }
        ],
        "status":Status,
        "question_type":Question_type,
        "total_vote": total_votes,
        "likes_count":like_count,
        "dislikes_count":dislike_count,
        "metaData":{
            "meta_title":person_name,
            "page_title":person_name,
            "meta_description":person_name,
            "meta_keywords":person_name,
            "meta_author":"Pollhole",
            "og_title":f"{person_name}'s Approval Rating",
            "og_image":person_image,
            "twitter_card":""
        }
}
    # print(data_create_poll)
    update_poll=re.post(f"{UP_POLL_URL}",json=data_create_poll,headers=head)
    print(update_poll.status_code)
    print(update_poll.json())

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
    new_image.show()
    new_image.save("updated_image.jpg")



def create_person_polls(): 
    with open(f"{filename_person}",'r',encoding="utf8") as csv_file:
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
                Question=i[1]
                Tags=i[2].split(",")
                Meta_keyword=i[3]
                Question_type=i[4]
                Status=i[5]
                Total_vote=taking_random_output_total_vote(i[6])
                # total_likes_dislikes=int(str(int(Total_vote)*int(taking_random_output_total_vote(i[7]))/100).split(".")[0])
                Likes_count=int(str(Total_vote*int(taking_random_output_total_vote(i[8]))/100).split(".")[0])
                Dislikes_count=Total_vote-Likes_count
                get_og_image(i[3])
                image_slug=Question.replace(" ","-").replace("?","")
                og_img=upload_to_aws("updated_image.jpg",'pollhole-metadata',f"{image_slug}_og_image.jpg")
                print(og_img)
                Og_image=og_img['url']
                print(Og_image)
                Person_poll_data()
                
                
                
                
                
def create_mcq_polls(): 
    with open(f"{filenamee}",'r',encoding="utf8") as csv_file:
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
            global Answer_1__vote_count
            global Answer_3__vote_count
            global Answer_2__vote_count
            global Og_image
            global Question_image
            global poll_ids
            poll_ids=[]
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
                grt_question_image()
                image_slug=Question.replace(" ","-").replace("?","")
                og_img=upload_to_aws("updated_image.jpg",'pollhole-metadata',f"{image_slug}_og_image.jpg")
                Og_image=og_img['url']
                question_img=upload_to_aws("question_image.jpg",'pollhole-metadata',f"{image_slug}_question_image.jpg")
                Question_image=question_img['url']
                print(Question_image)
                print(Og_image)
                mcq_poll_data()
    f= open("poll_ids.py","w") 
    f.write(str(poll_ids))  


filename_person()
create_person_polls()




