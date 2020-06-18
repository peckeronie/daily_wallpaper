import ctypes
import requests
from bs4 import BeautifulSoup
import os
import schedule
import time

def getImage(website):
    page = requests.get(website)
    html = BeautifulSoup(page.text, "html.parser")
    page.close()
    element = html.find("meta",  property="og:image")
    link = element["content"]
    return link 
    
def saveImage(link, folder):
    file_name = link.split("/")[-1]
    image_request = requests.get(link)
    if (os.path.isdir(folder) == False): #make folder to hold wallpaper images
        os.mkdir(folder)
    file_path = os.path.join(folder, file_name)
    print(file_path) 
    open(file_path, 'wb').write(image_request.content) #save the image into the folder
    image_request.close()
    print("image saved")
    return file_path

    
def setWallpaper(file_path, directory):
    
    pathname = os.fsdecode(file_path)
    print("Setting wallpaper...pathname:")
    print(pathname)
    extension = pathname.split('\\')[-1]
    print("Split pathname:")
    print(extension)
    for file in os.listdir(directory): #remove past wallpaper images in the folder
        filename = os.fsdecode(file)
        print("File:")
        print(filename)
        if filename != extension:
            print("Image not the same as newly downloaded image")
            os.remove(os.path.join(directory,file))
            print("Image removed")
        else:
            print("Image is the same")
            
    abs_path = os.path.abspath(file_path) #get absolute path for setting wallpaper   
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
    print(" ")
    print("Wallpaper set")

    
def setTags(tag_list):
    str1 = r"https://danbooru.donmai.us/posts/random?tags="
    for tag in tag_list:
        tag = tag.replace(' ', '_')
        str1 = str1 + tag + "+"
    str1 = str1[:-1]
    return str1
    
def main(list1,foldername):
    
    set_url = setTags(list1)
    pic_url = getImage(set_url)
    path = saveImage(pic_url, foldername)
    setWallpaper(path, foldername)

#set wallpaper at 5 am every day

some_tags = ["scenery","cherry blossoms"]
foldername = "wallpaperfolder"
schedule.every().day.at("05:00").do(main(some_tags, foldername))

while True:
    schedule.run_pending()
    time.sleep(1)
