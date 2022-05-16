import cv2
import sys
import os
from bs4 import BeautifulSoup
import datetime as dt
import random

cls_map = {'Car': 0, 'Human': 1, 'Motorcycle': 2, 'Bicycle': 3}


def load_annotation(file_path):
    """
    Load annotation file for a given image.
    Args:
        img_name (string): string of the image name, relative to
            the image directory.
    Returns:
        BeautifulSoup structure: the annotation labels loaded as a
            BeautifulSoup data structure
    """
    xml = ""
    with open(file_path, encoding='unicode_escape') as f:
        xml = f.readlines()
    xml = ''.join([line.strip('\t') for line in xml])
    return BeautifulSoup(xml)


folder_list = ['1-01d', '1-07d', '2-01d', '1-02d', '1-06d', '2-02d']

image_width = 640
image_height = 480

for folder in folder_list:
    folder_path = '/media/js/EVO_2TB/data/MUIN-reduced/DAY/{}'.format(folder)
    image_path = folder_path + '/rgbdepth/color'
    xml_path = folder_path + '/xml'
    save_path = folder_path + '/rgbdepth/label'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for root, dir, files in sorted(os.walk(image_path)):
        for file in sorted(files):
            if file.endswith('.png'):
                # img = cv2.imread(root + '/' + file)
                name = file.replace('RGB', "XML")
                name = name[:-4]
                if os.path.exists(xml_path + '/' + name + '.xml'):
                    annotation = load_annotation(xml_path + '/' + name + '.xml')

                save_label_file = "%s/%s.txt" % (save_path, file[:-4])
                f = open(save_label_file, 'w')

                print("file saved: %s" % (save_label_file))

                objs = annotation.findAll('object')
                for obj in objs:
                    bbox = obj.bndbox
                    cls = obj.find('name').contents[0]
                    xmin = int(bbox.xmin.contents[0])
                    ymin = image_height - int(bbox.ymin.contents[0])
                    xmax = int(bbox.xmax.contents[0])
                    ymax = image_height - int(bbox.ymax.contents[0])

                    if xmin < 0: xmin = 0
                    if ymin < 0: ymin = 0
                    if xmax < 0: xmax = 0
                    if ymax < 0: ymax = 0
                    if xmin > image_width: xmin = image_width
                    if ymin > image_height: ymin = image_height
                    if xmax > image_width: xmax = image_width
                    if ymax > image_height: ymax = image_height

                    x_center = (xmax + xmin) / 2.0 / image_width
                    y_center = (ymax + ymin) / 2.0 / image_height
                    width = abs(xmax - xmin) / image_width
                    height = abs(ymax - ymin) / image_height
                    f.write("%d %f %f %f %f\n" % (cls_map[cls], x_center, y_center, width, height))

                f.close()






