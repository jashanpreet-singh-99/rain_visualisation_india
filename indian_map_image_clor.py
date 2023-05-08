#!/usr/bin/env python
# coding: utf-8

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def create_map_india_with_state(color_list=None) :

    # DEFAULT COLOR LIST
    if color_list == None :
        color_list = [(198,75,220), (179,203,161), (85,1,91), (170,93,195), (136,91,169), (231,3,45), (13,28,155), (238,30,6), (170,31,141), (33,87,192), (27, 113,234), (254,128,177), (201,14,129), (66,182,35), (53,89,209), (158,193,11), (191,164,246), (108,6,168), (143,179,93), (121,60,32), (236,235,238), (106,225,238), (116,167,180), (3,75,121), (159,44,197), (202,43,96), (173,169,233), (118,209,217), (110,202,148), (51,70,240), (23,89,103)]

    # IMPORTS
    import os
    import cv2 as cv
    import numpy as np

    # PICK THE DEFAULT IMAGE AND GET REQUIRED PARAMETERS
    img_c = cv.imread(os.getcwd() +'/map_assets/map.png')
    img = cv.cvtColor(img_c, cv.COLOR_BGR2GRAY)
    x_m,y_m = img.shape
    print(x_m, y_m)

    # DIVIDE THE IMAGE ON BASES OF THRESHOLD OF 160 TO REMOVE NOISE
    for i in range(x_m) :
        for j in range(y_m) :
            if img[i,j] >= 160 :
                img[i,j] = 255
            else :
                img[i,j] = 0

    # FIND THE POSSIBLE ROI
    contours, _ = cv.findContours(img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = list(contours)
    area_index_dict = {}

    # GET THE AREA OF THE CONTOURS
    for i,contour in enumerate(contours):
        area = cv.contourArea(contour)
        area_index_dict[area] = i

    # FIND THE TOP AREAs
    top_28 = []
    for i,x in enumerate(sorted(area_index_dict.keys(), reverse=True)) :
        if i > 1:
            top_28.append(area_index_dict[x])
        elif i == 1:
            indian_boundary = area_index_dict[x]
        if i == 34:
            break

    # fixing the subdivision of the west bengal
    print(type(contours), len(contours[top_28[15]]))
    contours[top_28[15]] = np.concatenate((contours[top_28[15]],contours[top_28[25]]), axis=0)
    del top_28[25]
    # fixing the subdivision of andhra pradesh
    contours[top_28[5]] = np.concatenate((contours[top_28[5]],contours[top_28[29]]), axis=0)
    del top_28[29]
    # fixing the subdivision of tamil nadu
    contours[top_28[10]] = np.concatenate((contours[top_28[10]],contours[top_28[29]]), axis=0)
    del top_28[29]
    # fixing the subdivision of gujrat
    del top_28[29]

    # CREATE A NEW BLANK IMAGE
    new_img = np.zeros((750,662,3), dtype=np.uint8)
    new_img[:,:] = (220,220,220)
    print(new_img[100,100])

    # FILL THE REQUIRED COLORS
    for i,c_c in enumerate(top_28) :
        try:
            cv.drawContours(new_img, contours[c_c], -1, color_list[i], 5)
            cv.fillPoly(new_img, pts=[contours[c_c]], color=color_list[i])
        except:
            print("Error ", i)

    # SAVE IMAGE INTO FOLDER
    cv.imwrite( os.getcwd() + "/map_created/cur_map_img.png", new_img)

    return (os.getcwd() + "/map_created/cur_map_img.png" )

def get_stae_indexes() :
    # HARDCODED STATE WITH THEIR CONTOUR INDEX FROM THE TOP_LIST
    return {'rajasthan': 0, 'madhya pradesh': 1, 'maharastra': 2, 'jammu & kashmir': 3, 'uttar pradesh': 4, 'andhra pradesh': 5, 'gujarat': 6, 'Karnataka': 7, 'orrisa': 8, 'chhattisgarh': 9, 'tamil nadu': 10, 'bihar': 11, 'arunachal pradesh': 12, 'assam': 13, 'jharkhand': 14, 'west bengal': 15, 'himanchal pradesh': 16, 'uttaranchal': 17, 'punjab': 18, 'haryana': 19, 'kerala': 20, 'manipur': 21, 'meghalaya': 22, 'mizoram': 23, 'nagaland': 24, 'tripura': 25, 'sikkim': 26, 'goa': 27, 'delhi': 28}
