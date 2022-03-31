import os
import cv2
import pytesseract
import natsort
import pyttsx3
import json
import time

class ImgConvObj:
    def __init__(self, location, tes_config='-l eng'):
        self.location = location
        self.name = location.split("/")[-1].split("\\")[-1]
        self.images = self.get_files(location)
        self.text = ""
        self.tes_config = tes_config
    
    def get_files(self, location):
        files = os.listdir(location)
        imgs = []
        for file in files:
            end = file.split(".")[1]
            if end == "png" or end == "jpg" or end == "bmp":
                imgs.append(file)
        imgs = natsort.natsorted(imgs)
        return imgs
        
    def to_text(self):
        pytesseract.pytesseract.tesseract_cmd = 'Tesseract/tesseract.exe'
        temp_text = ""
        for img in self.images:
            load_img = cv2.imread(self.location + "/" + img)
            temp_text += pytesseract.image_to_string(load_img, config=self.tes_config)
        return temp_text.replace("\n", " ")
    
    def to_voice(self, config_dict):
        engine = pyttsx3.init()
        engine.setProperty('rate', int(config_dict["words_per_minute"])) 
        engine.setProperty('volume', float(config_dict["volume"]))
        voices = engine.getProperty('voices')
        if config_dict["voice"] == 'female':
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)
        engine.save_to_file(self.to_text(), self.location + '/' + config_dict["mp3_name"])
        engine.runAndWait()
    
config_file = open("Settings.config")
config_dict = json.load(config_file)
print("~~Config~~")
print("> mp3 name: " + config_dict["mp3_name"])
print("> words per minute: " + config_dict["words_per_minute"])
print("> volume: " + config_dict["volume"])
print("> voice: " + config_dict["voice"])
print()
loc_pics = input("Where are ur pics at: ")
loc_pics = loc_pics.split(',')
for folder in loc_pics:
    print("Processing " + folder.strip() + "...", end="\n")
    Image_Convert = ImgConvObj(folder.strip())
    Image_Convert.to_voice(config_dict)
    print("Finished")
print("All folders done, exiting...")
time.sleep(2)