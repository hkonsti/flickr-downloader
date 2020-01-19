import os

import requests
import re
import json
import shutil

import argparse

parser = argparse.ArgumentParser(description='Command line tool for bulk downloading flickr albums.')
parser.add_argument('-url', help='photo album url', dest='url')
parser.add_argument('-dir', help='directory to download to', dest='dir')

# go to main album page and find all image download urls
def find_images_infinite(url):
    # get album page
    result = requests.get(url)
    result = result.text

    # find and store api key for later use
    x = re.search(r"\"site_key\":\".{32}\",", result)
    api_key = result[x.start()+12:x.end()-2]

    # get album id for api request
    photosetid = url.split("/")[6]
    
    # creating empty array to match while condition
    temp_images = [None] * 50
    image_urls = []
    page = 1

    # loop through album 50 images at a time
    while len(temp_images) == 50:
        result = requests.get("https://api.flickr.com/services/rest?extras=can_addmeta%2Curl_o&per_page=50&page="+str(page)+"&primary_photo_extras=url_o%2C%20url_q%2C%20url_s%2C%20url_sq%2C%20url_t%2C%20url_z%2C%20needs_interstitial%2C%20can_share&photoset_id="+photosetid+"&method=flickr.photosets.getPhotos&api_key="+api_key+"&format=json&nojsoncallback=1")
        result = result.text

        result = json.loads(result)

        temp_images = result["photoset"]["photo"]

        for image in temp_images:
            image_urls.append(image["url_o"])

        page += 1

    return image_urls

# download image at the given url
def download(url):
    resp = requests.get(url, stream=True)
    local_file = open(parser.parse_args().dir+"/"+url.split("/")[4]+'.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp
    local_file.close()


if __name__ == "__main__":
    if parser.parse_args().url == None:
        raise Exception("No url specified. Please specify an album url. Use -h for more information.")

    if parser.parse_args().dir == None:
        raise Exception("No directory specified. Use -h for more information.")

    images = find_images_infinite(parser.parse_args().url)
    index = 1
    for image in images:
        download(image)
        print(str(int(index/len(images)*100))+"% -> Downloaded "+str(index)+" out of "+str(len(images)))
        index += 1
