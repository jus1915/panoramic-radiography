import os
import shutil
import json

#데이터 경로
path = "D:/data/구강안면/supervise"

folder_name_list = os.listdir(path)

#이미지, 어노테이션 파일에 각각 접근
for folder in folder_name_list:
    full_path = os.path.join(path,folder)
    path_img = os.path.join(full_path, 'img')
    path_ann = os.path.join(full_path, 'ann')
    print(os.listdir(path_img))
    print(os.listdir(path_ann))