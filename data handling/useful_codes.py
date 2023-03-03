import cv2
import numpy as np

#==============================================================================================

# 이미지 읽기(GrayScale로)
# img_array = np.fromfile(path_img, np.uint8)
# img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
# 높이 너비
# height, width = img.shape

# 이미지 저장
# cv2.imwrite(f"경로를 포함한 파일이름", img)

#==============================================================================================


# json 파일 열기
# with open(path_ann, 'r') as json_file:
#     ann = json.load(json_file)

#==============================================================================================

#이중 리스트 x좌표, y좌표 최대 최소값 구하기
# xmin_l = points[points[:, 0].argmin()][0]
# xmax_l = points[points[:, 0].argmax()][0]
# ymin_l = points[points[:, 1].argmin()][1]
# ymax_l = points[points[:, 1].argmax()][1]

#==============================================================================================

# 중심 좌표 구하고 margin만큼 확장된 영역 구하기
# x_c_l = int((xmin_l + xmax_l) / 2)
# y_c_l = int((ymin_l + ymax_l) / 2)
#
# w_l = xmax_l - xmin_l
# h_l = ymax_l - ymin_l
#
# left_x = int(x_c_l - margin * (w_l / 2))
# right_x = int(x_c_l + margin * (w_l / 2))
# bottom_y = int(y_c_l - margin * (h_l / 2))
# top_y = int(y_c_l + margin * (h_l / 2))

#==============================================================================================

#크롭된 이미지 생성
# img_l = img[bottom_y:top_y, left_x:right_x]
# mask_ian_l = mask_ian[bottom_y:top_y, left_x:right_x]
# mask_m3_l = mask_m3[bottom_y:top_y, left_x:right_x]

#==============================================================================================

# 마스크 이미지 생성
# height, width = img.shape
# mask_m3 = np.zeros((height, width))
# mask_ian = np.zeros((height, width))

#==============================================================================================

# 다각형 그리기(오목 다각형, 다각형, 선)
# mask_m3 = cv2.fillConvexPoly(mask_m3, points, 255)
# mask_m3 = cv2.fillPoly(mask_m3, [points], 255)
# mask_m3 = cv2.polylines(mask_m3, [points], isClosed=True, color=255, thickness=2)