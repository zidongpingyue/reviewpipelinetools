import json
import datetime
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request
import traceback
from . import Utils
import cv2
layoututilsblueprint=Blueprint('layoututils_blueprint',__name__)

import CardLayout
configparser=CardLayout.ConfigParser()
cardgenerator=CardLayout.CardGennerator((1000,1414))

@layoututilsblueprint.route('/generatelayout',methods=["POST"])
def GenerateLayout():    #显示所有员工信息
    try:
        json_dict=request.get_json()
        config_data= configparser.GenerateLayout((1000,1414),json_dict)
        imgs_card=cardgenerator.Simplelayout(config_data)
        imgs_base64=Utils.multi_img2base64(imgs_card)
        return jsonify(
            {
              "imgs_base64":imgs_base64
            }
        )
    except Exception as e:
        # print(e)
        traceback.print_exc()
        return jsonify(
            {
              "error":str(e)
            }
        )
    finally:
        pass