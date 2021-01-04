# convert mmdetection format to darknet format

import os
import json
import copy

from lxml import etree
from pathlib import Path

print("Starting conversion ...")
path = "/home/user/annotation/new/image"

# coco
sport_ball = 33  # from ball
person = 1       # from person

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
	miss_counter = 0

	for directory in os.listdir(path):
		base = os.path.join(path, directory)
		base_xml = os.path.join(base, 'xml')
		base_img = os.path.join(base, 'img')
		if os.path.isdir(base):
			print("Converting:", directory)

			counter = 0

			for file in sorted(os.listdir(base_xml)):

				meta = etree.parse(os.path.join(base_xml, file))
				file_name = meta.findall('filename')[0].text
				print(file_name)
				img_name = file_name.split(".")[0] + ".txt"
				new_annotation_file_name = os.path.join(base_img, img_name)

				objects = meta.findall('object')
				class_num = None
				x_center = None
				y_center = None
				width = None
				height = None
				frame_size = None

				frame_size = meta.findall('size')[0]
				frame_width = int(frame_size.findall('width')[0].text)
				frame_height = int(frame_size.findall('height')[0].text)

				if frame_size is None or frame_width == 0 or frame_height == 0:
					miss_counter += 1
					continue

				f = open(new_annotation_file_name, "w")

				for obj in objects:
					class_num = None
					class_in_xml = None
					class_in_xml = obj.findall('name')[0].text
					if class_in_xml:
						if class_in_xml == 'person' or class_in_xml == 'Person':
							class_num = person
						elif class_in_xml == 'ball' or class_in_xml == 'Ball':
							class_num = sport_ball

						if class_num:
							bndbox = obj.findall('bndbox')[0]
							x_min = int(bndbox.findall('xmin')[0].text) / frame_width
							y_min = int(bndbox.findall('ymin')[0].text) / frame_height
							x_max = int(bndbox.findall('xmax')[0].text) / frame_width
							y_max = int(bndbox.findall('ymax')[0].text) / frame_height

							x_center = (x_min + x_max) / 2
							y_center = (y_min + y_max) / 2
							width = x_max - x_min
							height = y_max - y_min

							# < bndbox >
							# < xmin > 2400 < / xmin >
							# < ymin > 387 < / ymin >
							# < xmax > 2422 < / xmax >
							# < ymax > 439 < / ymax >
							# < object -class > < x_center > < y_center > < width > < height >
							f.write(f"{class_num} {x_center} {y_center} {width} {height}\n")
						else:
							miss_counter += 1
					else:
						miss_counter += 1

				f.close()

				print("Processed", counter, "/", len(os.listdir(base)))
				counter += 1

	print(f"missed {miss_counter}")

if __name__ == "__main__":
    main()


