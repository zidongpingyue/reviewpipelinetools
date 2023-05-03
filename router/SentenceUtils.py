import json
import datetime
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request
import traceback
from . import Utils
import cv2
sentenceutilsblueprint=Blueprint('sentenceutils_blueprint',__name__)

import ModelLoader

@sentenceutilsblueprint.route('/rectifysentence',methods=["POST"])
def RectifySentence():    #显示所有员工信息
    try:
       
        return jsonify(
            {

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