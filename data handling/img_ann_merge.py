import os
import shutil
import json
from tqdm import tqdm
from pprint import pprint

#데이터 경로
path = "D:/data/panorama_radiography/supervise"

folder_name_list = os.listdir(path)

dest_img_path = "D:/data/panorama_radiography/img"
dest_ann_path = "D:/data/panorama_radiography/ann"

#이미지, 어노테이션 파일에 각각 접근
for folder in folder_name_list:
    full_path = os.path.join(path,folder)
    path_patient = os.path.join(full_path, 'img')
    patient_list = os.listdir(path_patient)

    for patient in tqdm(patient_list):

        dest_img = os.path.join(dest_img_path, f'{patient}')
        dest_ann = os.path.join(dest_ann_path, f'{patient}.json')

        path_img = os.path.join(full_path, f'img/{patient}')
        path_ann = os.path.join(full_path, f'ann/{patient}.json')

        shutil.copy(path_img, dest_img)
        shutil.copy(path_ann, dest_ann)