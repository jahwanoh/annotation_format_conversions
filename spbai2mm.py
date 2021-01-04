# convert superbAI export file to mmdetection format

import os
import json
import copy

from lxml import etree
from pathlib import Path

def read_xml(path):
    with tf.gfile.GFile(path, 'r') as fid:
            xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    return dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

print("Starting conversion ...")
path = "/home/user/annotation/new/meta"
path_label = "/home/user/annotation/new/labels"
path_data =  "/home/user/annotation/new/image"

def write_parameter(idx, root, obj):
	xml_obj = root.findall('object')
	if idx != 0:
		root.append(copy.deepcopy(xml_obj[0]))
		xml_obj = root.findall('object')

	xmin = int(obj["shape"]["box"]["x"])
	ymin = int(obj["shape"]["box"]["y"])
	xmax = int(obj["shape"]["box"]["x"] + obj["shape"]["box"]["width"])
	ymax = int(obj["shape"]["box"]["y"] + obj["shape"]["box"]["height"])

	if obj["class"] == "ball":
		root.findall('object')[idx][0].text = "ball"
	else:
		root.findall('object')[idx][0].text = "person"

	xml_obj[idx][-1][0].text = str(xmin)
	xml_obj[idx][-1][1].text = str(ymin)
	xml_obj[idx][-1][2].text = str(xmax)

	xml_obj[idx][-1][3].text = str(ymax)


def main():

	xml_template = etree.parse("template.xml")
	root = xml_template.getroot()

	# img, xml folder
	for	directory in os.listdir(path_data):
		base = os.path.join(path_data, directory)
		print("Ordering:", directory)
		img_path = base + "/img"
		xml_path = base + "/xml"
		Path(img_path).mkdir(parents=True, exist_ok=True)
		Path(xml_path).mkdir(parents=True, exist_ok=True)
		os.system(f"mv {base}/*.jpg {img_path}")
		os.system(f"ll {base}")

	for directory in os.listdir(path):
		base = os.path.join(path, directory)
		if os.path.isdir(base):
			print("Converting:", directory)

			counter = 0
			# project folder
			for file in sorted(os.listdir(base)):
				meta = json.load(open(os.path.join(base, file)))
				label_id = (meta["label_id"] + ".json")
				# ex) 0c98bd17-f931-4d41-a19f-f26b2222cefd.json
            				
				label = json.load(open(os.path.join(path_label, label_id)))
				objects = label["result"]["objects"]
     
				img_folder = meta["data_key"].split("_")[-2][-6:]
				# ex) 237136/"237136"_0111.jpg
				label_path = path_data + "/" + img_folder + "/xml"
				root.findall('folder')[0].text = path_data + "/" + img_folder + "/img"
				root.findall('filename')[0].text = meta["data_key"].split("/")[-1]  # ex) ~~/~~/*****_*****.jpg
				root.findall('size')[0][0].text = str(meta["image_info"]["width"])
				root.findall('size')[0][1].text = str(meta["image_info"]["height"])

				for idx, obj in enumerate(objects):
					write_parameter(idx, root, obj)

				# remove test before launch
				# label_path = directory + "/annotations/" + base
				
				Path(label_path).mkdir(parents=True, exist_ok=True)
				xml_template.write(label_path + "/" + meta["data_key"].split("/")[-1][:-4] + ".xml")

				print("Processed", counter, "/", len(os.listdir(base)))
				xml_template = etree.parse("template.xml")
				root = xml_template.getroot()
				counter += 1
				
                
					

if __name__ == "__main__":
    main()


