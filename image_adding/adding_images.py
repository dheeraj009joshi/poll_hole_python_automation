from PIL import Image
from image_adding.functions import add_images_4, upload_to_aws,add_images_2
image1 = 'https://pollhole-metadata.s3.amazonaws.com/guncontrol.jpg'
image2 = 'https://sportshub.cbsistatic.com/i/2022/01/02/8cf8f5a1-da48-4657-b146-c2d4b8c0c8eb/brock-lesnar-wwe-day-1.jpg'
image3 = 'https://assets.foxdcg.com/dpp-uploaded/images/wwe-friday-night-smackdown/chip_wwe_friday_night_smack_down_2022_b-keyart.jpg'
image4 = 'https://images.hindustantimes.com/rf/image_size_630x354/HT/p2/2020/04/09/Pictures/_01394fcc-7a43-11ea-9ef9-f1be7341055a.jpg'
image_slug='demo-image-pollhole-2-images.jpg'   
add_images_2(image2,image3,image_slug)
# upload_to_aws(image_slug, 'pollhole-metadata',image_slug)
print(f"https://pollhole-metadata.s3.amazonaws.com/{image_slug}")
