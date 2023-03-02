import os
import shutil
import json
from pprint import pprint

#데이터 경로
path = "D:/data/구강안면/supervise"

folder_name_list = os.listdir(path)

#이미지, 어노테이션 파일에 각각 접근
for folder in folder_name_list:
    full_path = os.path.join(path,folder)
    path_patient = os.path.join(full_path, 'img')
    patient_list = os.listdir(path_patient)

    for patient in patient_list:
        print(patient)
        path_img = os.path.join(full_path, f'img/{patient}')
        path_ann = os.path.join(full_path, f'ann/{patient}.json')
        with open(path_ann,'r') as file:
            ann = json.load(file)
        for object in ann['objects']:
            class_name = object['classTitle']
            points = object['points']['exterior']
            print(class_name)
            print(points)
        break
    break