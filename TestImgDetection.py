import cv2,os
from ImgDetection import ImageDetector

imagedetector=ImageDetector()
save_path="./img_data/img_detected/"
rected_path="./img_data/img_afterrec/"



img_list = sorted(os.listdir(rected_path))
for img_path in img_list:
        name = img_path.split('.')[-2]  # image name
        img_path = rected_path + img_path  # image path
        print("img_path:",img_path)
        # img=cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2RGB)
        img=cv2.imread(img_path)
        imgs_after,answers=imagedetector.ClipCardsAndDectectChara([img])
        print("answers:",answers)
        for index,img_after in enumerate(imgs_after):
            cv2.imwrite(save_path + name+str(index) + '_rec' + '.png',cv2.resize(img_after,(1000,1414)))