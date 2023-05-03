from CardLayout import CardGennerator,ConfigParser
import cv2
import TestData
layoutconfig=ConfigParser()
papergenerator=CardGennerator((1000,1414))
layout_= layoutconfig.GenerateLayout((1000,1414),TestData.testcardlayout)
imgs=papergenerator.Simplelayout(layout=layout_)
imgpath="./img_data/img_cards/"
for i,img in enumerate(imgs):
    filepath=f"{imgpath}/papercard_{i}.png"
    
    cv2.imwrite(filepath,img)
    print("save img:",filepath)
