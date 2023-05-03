import json
import sys
 
import cv2
import numpy as np
import CharaRecog
import re 
 
def preprocess(gray):
    sobel=gray.copy()
    # # 1. Sobel算子，x方向求梯度
    sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
    sobely = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize = 3)

    sobel=sobel.astype("uint8")
    cv2.addWeighted(sobelx,0.5,sobely,0.5,0,sobel)
    # sobel=sobel.astype("uint8")

    # sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
    # 2. 二值化
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    # ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_TOZERO+cv2.THRESH_BINARY)

    # 3. 膨胀和腐蚀操作的核函数

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # # 形态学操作             图像      操作（open）结构元素
    # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))

    element3 = cv2.getStructuringElement(cv2.MORPH_RECT, (30,9))
    element4 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    elementx = cv2.getStructuringElement(cv2.MORPH_RECT, (40,40))
    elementy = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
    # # 方案一：

    # # 先腐蚀
    # erosion = cv2.erode(binary, element1, iterations = 1)

    # # 再膨胀
    # dilation = cv2.dilate(erosion, element2, iterations = 2)

    # 方案二：
    # 直接膨胀
    # dilation = cv2.dilate(binary, element2, iterations = 1)

    # # 方案三（原方案）
    # # 4. 膨胀一次，让轮廓突出
    # dilation = cv2.dilate(binary, element4, iterations = 1)
 
    # # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    # erosion = cv2.erode(dilation, element3, iterations = 1)
 
    # # 6. 再次膨胀，让轮廓明显一些
    # dilation = cv2.dilate(erosion, element4, iterations = 3)

    # 方案四（成功）
    # 4. 膨胀一次，让轮廓突出
    # dilation = cv2.dilate(binary, elementx, iterations = 1)
 
    # # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    # erosion = cv2.erode(dilation, elementy, iterations = 1)
 
    # # 6. 再次膨胀，让轮廓明显一些
    # dilation = cv2.dilate(erosion, element4, iterations = 3)

    # 方案五
    elementx5 = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
    elementy5 = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    # 4. 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, elementx5, iterations = 1)
 
    # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    erosion = cv2.erode(dilation, elementy5, iterations = 1)
 
    # 6. 再次膨胀，让轮廓明显一些
    # dilation = cv2.dilate(erosion, elementx5, iterations = 3)

    # 7. 存储中间图片 
    # cv2.imencode('.png', binary)[1].tofile("二值化.png")
    # cv2.imencode('.png', dilation)[1].tofile("膨胀.png")
    # cv2.imencode('.png', erosion)[1].tofile("腐蚀.png")

    # result=dilation
    # result=binary
    result=erosion
    return result

def findTextRegion(img):
    
    region = []

    # 1. 查找轮廓
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)
    
    h_img,w_img=img.shape
    area_img=h_img*w_img

    # print(f"area_img:{area_img}")
    # 2. 筛选那些面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)

        # 面积小的都筛选掉

        if (area < area_img*0.1 or area>area_img*0.9):
            continue


        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 找到最小的矩形，该矩形可能有方向
        
        rect = cv2.minAreaRect(cnt)

        # box是四个点的坐标
        # imgs=cv2.imread("./img_rec/red1.png")
        box=cv2.boxPoints(rect)
        # for p in box:
        # #     # print(p)
        #     cv2.circle(imgs, (int(p[0]),int(p[1])), 10, (0, 0, 255), 2)
        # cv2.imencode('.png', imgs)[1].tofile("点.png") 
        # cv2.waitKey(0) #等待按键
        # cv2.destroyAllWindows()

        # box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        # if (height > width*1.2):
        #     continue
        
        # print(f'area:{area}')
        region.append(box)

        # print(region)

    return region

def detect(zip_image,img):
    # src=cv2.imread(imagePath)
    src=zip_image.copy()

    dilation = preprocess(img)
    # 3. 查找和筛选文字区域
    
    region = findTextRegion(dilation)
    area_list=[cv2.contourArea(r) for r in region]
    score_list=[i/max(area_list) for i in area_list]

    # print(score_list)
    # print(region)

    # dets=[[*i[0],*i[2]]+[1] for i in region]
    dets=[]
    # print(region)
    for r_i in range(len(region)):
        # ls=[min(r,key=lambda s[0]:s[0]+s[1])]
        # min_s=min(r,key=lambda s:s[0]+s[1])
        # print(f'min_s:{min_s}')

        r=region[r_i]
        min_s=None
        min_s_index=0
        for i in range(4):
            s=r[i][0]+r[i][1]
            if min_s==None or min_s>s:
                min_s=s
                min_s_index=i

        dets.append([*r[min_s_index],*r[(min_s_index+2)%4],score_list[r_i]])
    
    dets=np.array(dets)
    # print(dets)

    # 去除重复框
    index_list=py_cpu_nms(dets,0.2)
    # index_list=dets

    new_region=[]
    for index in index_list:
        new_region.append(region[index])
    
    # 对区域进行从上到下排序
    new_region.sort(key=lambda y:y[0][1])
    # print(new_region)
    # print(new_region)

    # 4. 用绿线画出这些找到的轮廓
    for box in new_region:
        cv2.drawContours(src, [box], 0 , (0, 255, 0), 2)
    
    # 5.文字识别
    answers=CharaRecog.result(zip_image,new_region)
    # with open('answers.json','w+',encoding='utf-8') as w:
    #     w.write(json.dumps(answers,ensure_ascii=False))

    # print(answers)
 
    # 带轮廓的图片
    # cv2.imencode('.png', src)[1].tofile("识别结果.png")
    
    #(识别后的单页,句子,框选区域)
    return (src,answers,new_region)

# 去重
def py_cpu_nms(dets, thresh):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    #按照从小到大排序后返回下标，然后顺序取反，即从大到小对应的下标
    order = scores.argsort()[::-1] 
    # print(f'norder:{order}')
    keep = []

    s=1
    while order.size > 0:
        i = order[0]
        keep.append(i)
        #求交叉面积intersection采用了这个非常巧妙的方法，自己画一下思考一下
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        # print(f'inter:{s} xx1:{xx1} yy1:{yy1} xx2:{xx2} yy2:{yy2}')

        w = np.maximum(0.0, xx2 - xx1 + 1) #计算w
        h = np.maximum(0.0, yy2 - yy1 + 1) #计算h
        # print(f'inter:{s} w:{w} h:{h}')

        inter = w * h       #交叉面积
        # print(f'inter:{s} {inter}')
        #A交B/A并B
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        # print(ovr)
        """
        保留重叠面积小于threshold的
        np.where的返回值是tuple
        第一个维度是x的list,第二个维度是y的list
        这里因为输入是1维,因此就取0就好
        """
        
        inds = np.where(ovr <= thresh)[0]

        # print(f'inds:{inds+1}')
        order = order[inds + 1]
        s+=1
        # print(f'order:{order}')
    # print(keep)
    return keep

# 检测红色区域
def DetectRedRegion(image):
    img = image

    img=cv2.resize(img,(1000,1414))
    # cv2.imencode('.png', img)[1].tofile("压缩.png")


    # # 去噪
    # img=cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

    # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # 从RGB色彩空间转换到HSV色彩空间
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)
 
    # H、S、V范围一：

    # 红色
    lower1 = np.array([0,43,46])
    upper1 = np.array([10,255,255])
    mask1 = cv2.inRange(grid_HSV, lower1, upper1)       # mask1 为二值图像
    res1 = cv2.bitwise_and(grid_RGB, grid_RGB, mask1)
 
    # H、S、V范围二：
    lower2 = np.array([156,43,46])
    upper2 = np.array([180,255,255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)
    res2 = cv2.bitwise_and(grid_RGB,grid_RGB, mask2)

    mask = mask1 + mask2
    
    # detect(imagePath,mask)
    return detect(img,mask)

# 检测黑色区域
def black(imagePath):
    img = cv2.imread(imagePath)
    # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # 从RGB色彩空间转换到HSV色彩空间
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

    # 黑色

    # 官方
    # lower1 = np.array([0,0,0])
    # upper1 = np.array([180,255,46])

    # 我的
    lower1 = np.array([0,0,0])
    upper1 = np.array([180,255,110])
    mask1 = cv2.inRange(grid_HSV, lower1, upper1)       # mask 为二值图像
    
    # # 灰色
    # lower2 = np.array([0,0,46])
    # upper2 = np.array([180,43,220])
    # mask2 = cv2.inRange(grid_HSV, lower2, upper2)       # mask 为二值图像

    # mask=mask1+mask2

    mask=mask1
    detect(imagePath,mask)

# 主函数入口,参数（[图片cv读取后],[]...）
def detect_multiple_imgs(imgs):
    answers_all=[]
    imgs_detected=[]
    # print("call--------------------------------------------------")
    print(len(imgs))
    for img in imgs:
        # print("img:",img.shape)
        img_detected,answer,_=DetectRedRegion(img)
        # print("343:",answer)
        answers_all=answers_all+answer
        imgs_detected.append(img_detected)

    temp_index=[]
    p1=r'续[\d]、'
    p2=r'[\d]、'
    for index,answer in enumerate(answers_all):
        t1=re.search(p1,answer)
        t2=re.search(p2,answer)
        if t1:
            temp_index.append(int(t1.group()[1]))
            answers_all[index]=answers_all[index][3::]
        elif t2:
            temp_index.append(int(t2.group()[0]))
            answers_all[index]=answers_all[index][2::]
        else:
            print("识别错误")

    result=[]
    now_index=-1
    for index,answer in zip(temp_index,answers_all):
        # print(index,answer)
        if now_index!=index:
            result.append(answer)
            now_index=index
        else:
            result[now_index-1]+=answer
    # print(fake,temp_index)
    # print(result)
    
    return (imgs_detected,answers_all)

    
class ImageDetector:
    def __init__(self) -> None:
        pass
    """
    ([img_clipped...],[answer_text...])
    """
    def ClipCardsAndDectectChara(self,imgs):
        return detect_multiple_imgs(imgs=imgs)