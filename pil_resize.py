#-*- coding: UTF-8 -*-
import os
import re
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def takeNum(elem):
    num = 0
    res = re.search('\((\d+)\)', elem)
    if res:
        num = res.groups(1)[0]
    #print(num)
    num = int(num)
    return num

def file_name(file_dir):
    model = []
    xiao = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg' and root == file_dir:
                if re.match('m', file) :
                    model.append(os.path.join(root, file))
                    #model.append(file)
                elif re.match('x', file):
                    xiao.append(os.path.join(root, file))
                else:
                    pass
    model.sort(key = takeNum)
    xiao.sort(key = takeNum)
    return model, xiao

def load_images():
    modellist, xiaolist = file_name("./")
    print(modellist, xiaolist)
    start = 1200
    bottom = 195
    mid = 55
    addlength, lenlist, imglist = calculate_length(modellist, mid)
    whole = start + addlength +bottom
    canvas = init_canvas(750, whole, color=(255, 255, 255))
    canvas = pintu(xiaolist, canvas)
    top = start
    canvas = addImg_h_w(canvas, imglist[0], top, 0)
    for i in range(1, len(modellist)):
        top = top + lenlist[i-1] + mid
        canvas = addImg_h_w(canvas, imglist[i], top, 0)
    return canvas

def pintu(xiaolist, canvas):
    height = 398
    width = 267
    zuoyou = 60
    shangxia = 31
    top1 = 114
    left1 = 78
    right1 = left1 + width
    top2 = top1
    left2 = left1 + width + zuoyou
    right2 = 750
    left3 = left1
    right3 = right1
    top3 = top1 + height + shangxia
    bottom3 = top3 + height
    left4 = right3 + zuoyou
    top4 = top3
    cut_image = []
    for i in range(0, len(xiaolist)):
        image =  Image.open(xiaolist[i])
        cut_image.append(resize_cut(image, width, height))
    canvas = addImg_h_w(canvas, cut_image[0], top1, left1)
    canvas = addImg_h_w(canvas, cut_image[1], top2, left2)
    canvas = addImg_h_w(canvas, cut_image[2], top3, left3)
    canvas = addImg_h_w(canvas, cut_image[3], top4, left4)
    return canvas

def calculate_length(modellist, mid):
    imagelist = []
    lenlist = []
    length = 0
    #mid = 55
    #start = 1200
    for file in modellist:
        image =  Image.open(file)
        h, w = image.size
        needh = int(750*w/h)
        textx = 196
        if h < w:
            texty = int(needh * 0.93)
        else:
            texty = int(needh * 0.85)
        length = length + needh + mid
        resized = resize_cut(image, 750, needh)
        print(resized.size)
        new = add_text(resized, textx, texty)
        lenlist.append(needh)
        print(file, w, h, needh, length)
        imagelist.append(new)
    return length - mid, lenlist, imagelist

def resize_cut(image, width, height):
    top, bottom, left, right = (0, 0, 0, 0)

    #获取图像尺寸
    # h, w, _ = image.shape
    w, h = image.size

    #计算需要裁的边
    # longest_edge = max(h, w)
    h_need = height * w / width
    w_need = width * h / height
    if h > h_need: #上下需要裁
        top = int((h - h_need)/2)
        bottom = int(h_need + (h - h_need)/2)
        left = 0
        right = w
    elif h < h_need: #左右需要裁
        top = 0
        bottom = h
        left = int((w - w_need)/2)
        right = int(w_need + (w - w_need)/2)
    else:
        right = w
        bottom = h
    # print("left, right, top, bottom: ",left,right,top,bottom)
    box = (left, top, right, bottom)
    region = image.crop(box)
    # cropImg = image[top:bottom,left:right] # 裁剪坐标为[y0:y1, x0:x1]

    #调整图像大小并返回
    # return cv2.resize(cropImg, (height, width))
    return region.resize((width, height), Image.ANTIALIAS)
    # return region.resize((width, height))

def init_canvas(width, height, color=(255, 255, 255)):
    canvas = np.ndarray((height, width, 3), dtype="uint8")
    canvas[:] = color
    canvas = Image.fromarray(canvas)
    return canvas

def addImg(img1, img2, top, bottom, left, right):
    img1[top:bottom,left:right] = img2       #图像替换
    return img1

def addImg_h_w(img1, img2, top, left):
    # newimg2 = resize_cut(img2, height, width)
    #img1[top:top+height,left:left+width] = img2
    img1.paste(img2, (left,top))
    return img1

def add_text(image, x, y):
    font = ImageFont.truetype("COPRGTL.TTF", 37, encoding="unic")#设置字体
    draw = ImageDraw.Draw(image)
    draw.text((x, y), 'C    U    L    T    U    M', 'white', font)  #左上角为(0,0)
    return image

def pathname():
    pwdpath = os.getcwd()
    name = pwdpath.split(os.sep)[-1]
    return name
    
def main():
    # 调整图片大小
    newname = pathname() + '.jpg'
    print(newname)
    canvas = load_images()
    canvas.save(newname, quality=100)

if __name__ == "__main__":
    main()
