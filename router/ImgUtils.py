import json
import datetime
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request
import traceback
from . import Utils
import cv2
imgutilsblueprint=Blueprint('imgutils_blueprint',__name__)

import ModelLoader

# @imgutilsblueprint.route('/rectifyimg',methods=["POST"])
# def RectifyImage():    #显示所有员工信息
#     try:

#         return jsonify(
#             {

#             }
#         )
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         return jsonify(
#             {
#               "state":str(e)
#             }
#         )
#     finally:
#         pass
"""
{
    imgs_base64:[...,...]
}
"""
@imgutilsblueprint.route('/testimg',methods=["POST"])
def RectifyImage01():    #显示所有员工信息
    try:
        json_dict=request.get_json()
        imgs_base64=json_dict["imgs_base64"]
        
        hashs=[]
        for index,img_base64 in enumerate(imgs_base64):
            img,buffer=Utils.base64toimg(img_base64)
            hashcode=Utils.bytes2hash(buffer)
            filename=f"./img_data/img_base64/{index}_{hashcode[0:10]}.jpg"
            print("filename",filename)
            cv2.imwrite(filename,img)
            hashs.append(hashcode)
        return jsonify(
            {
               "img_hashs":hashs
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":str(e)
            }
        )
    finally:
        pass
@imgutilsblueprint.route('/rectifyimg',methods=["POST"])
def RectifyImage():    #显示所有员工信息
    try:
        json_dict=request.get_json()
        imgs_base64=json_dict["imgs_base64"]
        imgs_rectified=[]
        #矫正图片
        for img_base64 in imgs_base64:
            img,buffer=Utils.base64toimg(img_base64)
            hashcode=Utils.bytes2hash(buffer)
            img_rectified=ModelLoader.utilmodels.DocRectify.rectify(img)
            imgs_rectified.append((img_rectified,hashcode))
        
        return jsonify(
            {
              "hashcodes":[hashcode for img_rectified,hashcode in imgs_rectified],
              "imgs_base64":[Utils.img2base64(img_rectified)[0] for img_rectified,hashcode in imgs_rectified]
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":str(e)
            }
        )
    finally:
        pass
@imgutilsblueprint.route('/detectimg',methods=["POST"])
def DetectImage():    #显示所有员工信息
    try:
        json_dict=request.get_json()
        imgs_base64=json_dict["imgs_base64"]
        # print("imgs_base64:",len(imgs_base64))
        
        imgs,imgs_buffer=Utils.multi_base64toimg(imgs_base64)
        # print("imgs:",len(imgs))
        imgs_detected,answers_text=ModelLoader.utilmodels.ImgAchorAndCharaDetection.ClipCardsAndDectectChara(imgs)
        print("anstext:",answers_text)
        return jsonify(
            {
                "answers_text":answers_text
            }
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "state":str(e)
            }
        )
    finally:
        pass