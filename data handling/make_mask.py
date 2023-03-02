import os
import shutil
import json
import numpy as np
from pprint import pprint
import cv2
from tqdm import tqdm
from PIL import Image
#데이터 경로
path = "D:/data/panorama_radiography/supervise"

folder_name_list = os.listdir(path)

#이미지, 어노테이션 파일에 각각 접근
for folder in tqdm(folder_name_list):
    full_path = os.path.join(path,folder)
    path_patient = os.path.join(full_path, 'img')
    patient_list = os.listdir(path_patient)

    for patient in tqdm(patient_list):
        path_img = os.path.join(full_path, f'img/{patient}')
        path_ann = os.path.join(full_path, f'ann/{patient}.json')

        #이미지 읽기(GrayScale로)
        img_array = np.fromfile(path_img, np.uint8)
        img = cv2.imdecode(img_array,  cv2.IMREAD_GRAYSCALE)

        #마스크 이미지 생성
        height, width = img.shape
        mask_m3 = np.zeros((height,width))
        mask_ian = np.zeros((height,width))

        with open(path_ann,'r') as file:
            ann = json.load(file)
        for object in ann['objects']:
            class_name = object['classTitle']
            points = object['points']['exterior']
            points = np.array(points)
            if class_name == '#38':
                mask_m3 = cv2.fillConvexPoly(mask_m3, points, 255)
            if class_name == '#48':
                mask_m3 = cv2.fillConvexPoly(mask_m3, points, 255)
            if class_name == 'Lt.N':
                mask_ian = cv2.fillConvexPoly(mask_ian, points, 255)
            if class_name == 'Rt.N':
                mask_ian = cv2.fillConvexPoly(mask_ian, points, 255)

        cv2.imshow(patient,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow(patient, mask_m3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow(patient, mask_ian)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    #     break
    # break