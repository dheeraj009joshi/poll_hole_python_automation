from email.mime import application
import json
from regex import A
import requests as re
from PIL import Image
from requests_oauthlib import OAuth1
from image_adding.functions import add_images_4, upload_to_aws,add_images_2
from config import ACCESS_TOKEN, BASE_URL,UP_POLL_URL
Data={
  "status": 1,
  "question_type":2,
  "og_image_filter":True
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = re.post(BASE_URL, data=json.dumps(Data), headers=headers)
aa=len((r.json())["data"][0]["answers"])
# print(r.json()["data"][0]["answers"])[0]
question=str(r.json()["data"][0]["question"]).replace(" ","-")
image1 = r.json()["data"][0]["answers"][0]["image"]
image2 = r.json()["data"][0]["answers"][1]["image"]
image3 = r.json()["data"][0]["answers"][2]["image"]
image4 = r.json()["data"][0]["answers"][3]["image"]
image_slug=f'{question}.png'   
add_images_4(image1,image2,image4,image3,"output.png")
upload_to_aws("output.png", 'pollhole-metadata',image_slug)
print(f"https://pollhole-metadata.s3.amazonaws.com/{image_slug}")

updated_image=(f"https://pollhole-metadata.s3.amazonaws.com/{image_slug}")

poll_id=r.json()["data"][0]["_id"]
print(poll_id)
data_update_poll={ 
    "metaData": {
              "og_image": updated_image
            }
}
head = {"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyODY5OWJhOGJlNDMxMzBiY2JlZWJhNCIsImlhdCI6MTY1MzM3MTQ5NH0.33bFu_aC-lvJoPG4l6GF7s4Tfi20V4FYoiz6yz2qiBY"}
update_poll=re.put(f"{UP_POLL_URL}/{poll_id}",json=data_update_poll,headers=head)
print(update_poll.url)
print(update_poll.json())


