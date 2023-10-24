import requests
import lxml
from bs4 import BeautifulSoup
from PIL import Image
import img2pdf
import os
from dotenv import load_dotenv
import ast
import json
from transliterate import translit, get_available_language_codes
import numpy as np
import cv2
import time
import random

load_dotenv()

url = "https://pereborom.ru/dzhazovye-akkordy-na-gitare/"

# env variable
headers_string = os.getenv('HEADERS')
# conversion to dict 
headers = ast.literal_eval(headers_string)

# replacing characters with _
def name_decorate(name):
    rep = ["'", ".", " ", ",", "-"]
    for word in name:
        if word in rep:
            name = name.replace(word, "_")
    return name
#  write image to pdf
def write_to_pdf():
    with open("data/chords.pdf", "wb") as f:
        f.write(img2pdf.convert(image_list))
# the image is deleted or added to the list
def img_check(img):
    if image_comparsion("example.png", img) > 60:
        os.remove(img)
    else:
        image_list.append(img)
        print("Image is saved...")
        
        
# image comparison
def image_comparsion(img1_path, img2_path):
    # open images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    # Resize the images
    img_size = (img1.shape[1], img1.shape[0])
    img2 = cv2.resize(img2, img_size)
    
    # Mean Squared Error
    mse = np.mean((img1 - img2) ** 2)
    
    return mse
# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w", encoding="utf8") as f:
#     f.write(src)
    
# with open("index.html", encoding="utf8") as f:
#     src = f.read()
    
# soup = BeautifulSoup(src, "lxml")
# # images search
# all_images = soup.find_all(class_="size-full")
# all_images_dict = {}
# # image sort
# for image in all_images:
#     name = translit(name_decorate(image.get("alt")), "ru", reversed=True)
#     image_href = image.get("src")
    
#     all_images_dict[name] = image_href

# saving in json    
# with open("all_images.json", "w", encoding="utf8") as f:
#     json.dump(all_images_dict, f, indent=4, ensure_ascii=False)

# a function that takes a json file for parsing

image_list = []

def img_parsing(json_file):
    with open(json_file, encoding="utf8") as f:
        all_images = json.load(f)
        
    count = 1

    for img_name, img_href in all_images.items():

        img_response = requests.get(img_href, stream=True)
        img = Image.open(img_response.raw)
        img.save(f"data/media/{img_name}.png")
        
        print(f"Image {count} save...")
        time.sleep(random.randrange(2,4))
        
        img_check(f"data/media/{img_name}.png")
        print(f"Image {count} complete...")
        count += 1
        
    print("Create a pdf document")
    time.sleep(random.randrange(1,2))
    write_to_pdf()
    
    print("*" * 20)
    print("Done")

if __name__ == "__main__":
    img_parsing("all_images.json")