# matching check between images and xml files

import os
import json
import copy

from lxml import etree
from pathlib import Path

print("Starting conversion ...")
path = "/home/user/annotation/new/image"
path_new = "/home/user/annotation/new/dataset"

def main():

    for directory in os.listdir(path):
        base = os.path.join(path, directory)
        if os.path.isdir(base):
            print("checking:", directory)

            new_path = path_new + "/" + directory 
            Path(new_path).mkdir(parents=True, exist_ok=True)
            Path(new_path + "/img").mkdir(parents=True, exist_ok=True)
            Path(new_path + "/xml").mkdir(parents=True, exist_ok=True)
   
            counter = 0
			
            # if base.split("/")[-1] == "dataset" or base.split("/")[-1] == "water-melon" or base.split("/")[-1] == "superbai-2020-10":
            #     continue
            
            for xml_file in sorted(os.listdir(base + "/xml")):
                
                img_file = xml_file.split(".")[0] + ".jpg"
    
                xml_full_path = base + "/xml/" + xml_file
                img_full_path = base + "/img/" + img_file
                xml_full_new_path = new_path + "/xml/" + xml_file
                img_full_new_path = new_path + "/img/" + img_file                   
                if os.path.isfile(img_full_path):
                    #move
                    os.system(f"cp {xml_full_path} {xml_full_new_path}")
                    os.system(f"cp {img_full_path} {img_full_new_path}")
                 
                print("Processed", counter, "/", len(os.listdir(base + "/xml")))
                counter += 1
                
if __name__ == "__main__":
    main()


