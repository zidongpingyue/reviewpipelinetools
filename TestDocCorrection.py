from DocCorrection import DocCorrector
import cv2
import os
corrector=DocCorrector()
# img=cv2.imread("./test/test06.jpg")
# img_after=corrector.rectify(img)
# cv2.imwrite("./test/test06_rec.jpg",cv2.resize(img_after,(1000,1414)))

distorrted_path="./img_data/img_distort/"
save_path="./img_data/img_rec/"
img_list = sorted(os.listdir(distorrted_path))
for img_path in img_list:
        name = img_path.split('.')[-2]  # image name
        img_path = distorrted_path + img_path  # image path
        print("img_path:",img_path)
        img=cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2RGB)
        img_after=corrector.rectify(img)
        cv2.imwrite(save_path + name + '_rec' + '.png',cv2.resize(img_after,(1000,1414)))