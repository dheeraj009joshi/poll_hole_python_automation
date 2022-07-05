import json
from selenium import webdriver
import time
import requests as re
from config import ACCESS_TOKEN, UP_POLL_URL
driver=webdriver.Chrome("chromedriver.exe")
driver.get("https://en.wikipedia.org/wiki/Category:WWE_Hall_of_Fame_inductees")
time.sleep(5)
Name=driver.find_elements_by_xpath('//*[@id="mw-pages"]/div/div/div/ul/li/a')
names=[]
def create_poll(person_name,person_image):
    head = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data_create_poll={
        "creater_id":"628699ba8be43130bcbeeba4",
        "question":person_name,
        "question_type":int(3),
        "tags":[{
            "tag_name":"WWE Hall Of Fame"

        }],
            "answers":[
        {

            "image":person_image
        }
        ],
        "status":3,
        "question_type":3,
        "total_vote": 0,
        "likes_count": 0,
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

for ni in Name:
    names.append(ni.text)
for n in names:
    driver.get(f'https://en.wikipedia.org/wiki/{n.replace(" ","_")}')
    # driver.get(f'https://en.wikipedia.org/wiki/Abdullah_the_Butcher')
    time.sleep(2)
    try:

        try:
            person_name=driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[1]/th/div').text
            person_image=driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[2]/td/a/img').get_attribute('src')
            print("person= "+person_name)
            print("person_image= "+person_image)
            create_poll(person_name,person_image)
            print()
            print()
            time.sleep(5)
        except:
            
            person_name=driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/th').text
            person_image=driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[2]/td/a/img').get_attribute('src')
            print("person= "+person_name)
            print("person_image= "+person_image)
            create_poll(person_name,person_image)
            print()
            print()
            time.sleep(5)
    except Exception as e :
        print(e)
        pass

