import json
import datetime
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request
import traceback
from . import Utils
import cv2


class PipelineTask:
      def __init__(self,execute_fn) -> None:
           self.execute_fn=execute_fn
           pass
class WorkPipeline:
      def __init__(self) -> None:
          self.pipeline=[]
          self.context={}
          self.currenttask:PipelineTask
          pass
      def runpipeline(self,init_data:dict):
          self.context=init_data
          for task in self.pipeline:
              self.context=task.execute_fn(self.context)
          return self.context
          pass
      def addpipelinetask(self,execute_fn):
          task_=PipelineTask(execute_fn=execute_fn)
          self.pipeline.append(task_)
          return self
          pass
          

       



workpipelineblueprint=Blueprint('workpipeline_blueprint',__name__)

import ModelLoader
"""
json => {"workstate","imgs_base64","imgs_hash","question_answers"}
"""
def parsetask(context):
    imgs_raw,imgs_buffer=Utils.multi_base64toimg(context["imgs_base64"])
    imgs_hash=Utils.multi_bytes2hash(imgs_buffer)
    context={
        "workstate":"parsetask",
        "imgs_raw":imgs_raw,
        "imgs_hash":imgs_hash
    }
    return context
    
def imgrecttask(context):
    imgs_raw=context["imgs_raw"]
    imgs_hash=context["imgs_hash"]
    
    imgs_rectified=[ModelLoader.utilmodels.DocRectify.rectify(
        cv2.cvtColor(img_raw,cv2.COLOR_BGR2RGB)
        ) for img_raw in imgs_raw]
    context={
        "workstate":"imgrecttask",
        "imgs_rectified":imgs_rectified,
        "imgs_hash":imgs_hash
    }
    return context

def imgdetecttask(context):
    imgs_rectified=context["imgs_rectified"]
    imgs_detected,texts_answer=ModelLoader.utilmodels.ImgAchorAndCharaDetection.ClipCardsAndDectectChara(imgs_rectified)
    context={
        "workstate":"imgdetecttask",
        "imgs_detected":imgs_detected,
        "texts_answer":texts_answer,
    }
    return context

def packinfotesttask(context):
    context={
        "workstate":"packinfo",
        "texts_answer":context["texts_answer_corrected"]
    }
    return context
def sentencecorrecttask(context):
    
    texts_answer_corrected=[]
    for text_answer in context["texts_answer"]:
        texts_answer_corrected.append(ModelLoader.utilmodels.SentenceCorrection.sentencecorrect(text_answer))
    context={
        "workstate":"sentencecorrect",
        "texts_answer_corrected":texts_answer_corrected,
    }
    return context

@workpipelineblueprint.route('/runworkpipeline',methods=["POST"])
def DetectImage():    #显示所有员工信息
    workpipeline=WorkPipeline()
    try:
        
        
        json_dict=request.get_json()
        # imgs_base64=json_dict["imgs_base64"]
        workpipeline.addpipelinetask( parsetask)\
        .addpipelinetask(imgrecttask)\
        .addpipelinetask(imgdetecttask)\
        .addpipelinetask(sentencecorrecttask)\
        .addpipelinetask(packinfotesttask)
        

        workpipeline.runpipeline(json_dict)
    
        print("anstext:",workpipeline.context)
        return jsonify(
            {
                "workstate":workpipeline.context["workstate"],
                **workpipeline.context
            }
        )
    except Exception as e:
        # print(e)
        traceback.print_exc()
        return jsonify(
            {
                "workstate":workpipeline.context["workstate"],
                "error":str(e)
            }
        )
    finally:
        pass