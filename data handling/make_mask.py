import os
import shutil
import json
import numpy as np
from pprint import pprint
import cv2
from tqdm import tqdm
from PIL import Image

#데이터 경로
path = "D:/data/panorama_radiography"

file_list = os.listdir(f"{path}/img")

#이미지, 어노테이션 파일에 각각 접근
for file in tqdm(file_list):
    path_img = os.path.join(path, f'img/{file}')
    path_ann = os.path.join(path, f'ann/{file}.json')

    #이미지 읽기(GrayScale로)
    img_array = np.fromfile(path_img, np.uint8)
    img = cv2.imdecode(img_array,  cv2.IMREAD_GRAYSCALE)

    xmin_l = 0
    xmax_l = 0
    ymin_l = 0
    ymax_l = 0

    xmin_r = 0
    xmax_r = 0
    ymin_r = 0
    ymax_r = 0

    bool_m3_l = False
    bool_m3_r = False
    bool_ian_l = False
    bool_ian_r = False

    #마스크 이미지 생성
    height, width = img.shape
    mask_m3 = np.zeros((height,width))
    mask_ian = np.zeros((height,width))

    margin = 1.5

    with open(path_ann,'r') as json_file:
        ann = json.load(json_file)

    for object in ann['objects']:
        class_name = object['classTitle']
        points = object['points']['exterior']
        points = np.array(points)

        if class_name == '#38':
            bool_m3_l = True
            # crop을 위한 m3의 width, height, center 찾기

            xmin_l = points[points[:,0].argmin()][0]
            xmax_l = points[points[:,0].argmax()][0]

            ymin_l = points[points[:,1].argmin()][1]
            ymax_l = points[points[:,1].argmax()][1]

            # mask_m3 = cv2.fillConvexPoly(mask_m3, points, 255)
            mask_m3 = cv2.fillPoly(mask_m3, [points], 255)
            mask_m3 = cv2.polylines(mask_m3, [points], isClosed=True, color=255, thickness=2)

        if class_name == '#48':
            bool_m3_r = True
            # crop을 위한 m3의 width, height, center 찾기
            xmin_r = points[points[:,0].argmin()][0]
            xmax_r = points[points[:,0].argmax()][0]

            ymin_r = points[points[:,1].argmin()][1]
            ymax_r = points[points[:,1].argmax()][1]

            # mask_m3 = cv2.fillConvexPoly(mask_m3, points, 255)
            mask_m3 = cv2.fillPoly(mask_m3, [points], 255)
            mask_m3 = cv2.polylines(mask_m3, [points], isClosed=True, color=255, thickness=2)

        if class_name == 'Lt.N':
            bool_ian_l = True
            # mask_ian = cv2.fillConvexPoly(mask_ian, points, 255)
            mask_ian = cv2.fillPoly(mask_ian, [points], 255)
            mask_ian = cv2.polylines(mask_ian, [points], isClosed=True, color=255, thickness=2)

        if class_name == 'Rt.N':
            bool_ian_r = True
            # mask_ian = cv2.fillConvexPoly(mask_ian, points, 255)
            mask_ian = cv2.fillPoly(mask_ian, [points], 255)
            mask_ian = cv2.polylines(mask_ian, [points], isClosed=True, color=255, thickness=2)

    mask_and = cv2.bitwise_and(mask_m3, mask_ian)
    mask_or = cv2.bitwise_or(mask_m3, mask_ian)

    if bool_m3_l and bool_ian_l:
        x_c_l = int((xmin_l + xmax_l) / 2)
        y_c_l = int((ymin_l + ymax_l) / 2)

        w_l = xmax_l - xmin_l
        h_l = ymax_l - ymin_l

        left_x = int(x_c_l-margin*(w_l/2))
        right_x = int(x_c_l+margin*(w_l/2))
        bottom_y = int(y_c_l-margin*(h_l/2))
        top_y = int(y_c_l+margin*(h_l/2))

        if left_x < 0 or right_x > width or bottom_y < 0 or top_y > height or right_x-left_x > width/2:
            continue

        img_l = img[bottom_y:top_y,left_x:right_x]
        mask_ian_l = mask_ian[bottom_y:top_y,left_x:right_x]
        mask_m3_l = mask_m3[bottom_y:top_y,left_x:right_x]

        # print(f"{file[:-4]}_l.png", f"img shape : {img.shape} left_x:{left_x} right_x:{right_x} bottom_y:{bottom_y} top_y:{top_y}")
        cv2.imwrite(f"{path}/crop/ian/{file[:-4]}_l.png",mask_ian_l)
        cv2.imwrite(f"{path}/crop/m3/{file[:-4]}_l.png",mask_m3_l)
        cv2.imwrite(f"{path}/crop/img/{file[:-4]}_l.png",img_l)

    if bool_m3_r and bool_ian_r:
        x_c_r = int((xmin_r + xmax_r) / 2)
        y_c_r = int((ymin_r + ymax_r) / 2)

        w_r = xmax_r - xmin_r
        h_r = ymax_r - ymin_r

        left_x = int(x_c_r-margin*(w_r/2))
        right_x = int(x_c_r+margin*(w_r/2))
        bottom_y = int(y_c_r-margin*(h_r/2))
        top_y = int(y_c_r+margin*(h_r/2))

        if left_x < 0 or right_x > width or bottom_y < 0 or top_y > height:
            continue

        img_r = img[bottom_y:top_y,left_x:right_x]
        mask_ian_r = mask_ian[bottom_y:top_y,left_x:right_x]
        mask_m3_r = mask_m3[bottom_y:top_y, left_x:right_x]

        # cv2.imshow("img_r", img_r)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #
        # cv2.imshow("mask_r", mask_ian_r)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #
        # cv2.imshow("mask_r", mask_m3_r)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print(f"{file[:-4]}_r.png", f"img shape : {img.shape} left_x:{left_x} right_x:{right_x} bottom_y:{bottom_y} top_y:{top_y}")
        cv2.imwrite(f"{path}/crop/ian/{file[:-4]}_r.png",mask_ian_r)
        cv2.imwrite(f"{path}/crop/m3/{file[:-4]}_r.png",mask_m3_r)
        cv2.imwrite(f"{path}/crop/img/{file[:-4]}_r.png",img_r)

    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # cv2.imshow("mask_m3", mask_m3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # cv2.imshow("mask_ian", mask_ian)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()