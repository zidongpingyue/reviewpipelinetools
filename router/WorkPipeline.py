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
          self.pass_context={}
          self.non_pass_context={}
          self.currenttask:PipelineTask
          pass
      def runpipeline(self,pass_init_data:dict,global_init_data:dict):
          self.pass_context=pass_init_data
          self.non_pass_context=global_init_data
          for task in self.pipeline:
              self.pass_context=task.execute_fn(self.pass_context,self.non_pass_context)
          return self.pass_context
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
def parsetask(context,non_pass_context):
    imgs_raw,imgs_buffer=Utils.multi_base64toimg(context["imgs_base64"])
    imgs_hash=Utils.multi_bytes2hash(imgs_buffer)
    context={
        "workstate":"parsetask",
        "imgs_raw":imgs_raw,
        "imgs_hash":imgs_hash
    }
    non_pass_context["imgs_hash"]=imgs_hash
    return context
    
def imgrecttask(context,non_pass_context):
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

def imgdetecttask(context,non_pass_context):
    imgs_rectified=context["imgs_rectified"]
    imgs_detected,texts_answer=ModelLoader.utilmodels.ImgAchorAndCharaDetection.ClipCardsAndDectectChara(imgs_rectified)
    context={
        "workstate":"imgdetecttask",
        "imgs_detected":imgs_detected,
        "texts_answer":texts_answer,
    }
    return context


def sentencecorrecttask(context,non_pass_context):
    
    texts_answer_corrected=[]
    for text_answer in context["texts_answer"]:
        texts_answer_corrected.append(ModelLoader.utilmodels.SentenceCorrection.sentencecorrect(text_answer))
    context={
        "workstate":"sentencecorrect",
        "texts_answer_corrected":texts_answer_corrected,
        "texts_answer":context["texts_answer"]
    }
    return context
def sentencejudgetask(context,non_pass_context):
    textarrays_question_answer=non_pass_context["question_answer"]
    texts_answer=[]
    if "texts_answer_corrected" in context:
        for texts in context["texts_answer_corrected"]:
            texts_only=[text_split[0] for text_split in texts ] 
            texts_answer.append("，".join(texts_only))
    else :
        texts_answer=context["texts_answer"]
    review_result=[]
    for question_index,texts_standard_answer in enumerate(textarrays_question_answer):
        question_result=[]
        text_answer=texts_answer[question_index]
        for point_index,text_standard_answer_pack in enumerate(texts_standard_answer):
            # print("long:",text_answer,"short:",text_standard_answer)
            text_standard_answer=text_standard_answer_pack[0]
            text_standard_answer_score=int(text_standard_answer_pack[1])
            score,entails=ModelLoader.utilmodels.SentenceMatch.CalculateScore(text_answer,text_standard_answer)
            question_result.append({"keysentence":text_standard_answer,"score":str(int(score)*text_standard_answer_score),"entails":list(entails)})
        review_result.append(question_result)
    context={
        "workstate":"sentencejudge",
        "result":review_result,
        "texts_answer":texts_answer
    }
    return context
def packinfotesttask(context,non_pass_context):
    context={
        "workstate":"packinfo",
        "texts_answer":context["texts_answer"],
        "result":context["result"]
    }
    return context

@workpipelineblueprint.route('/runworkpipeline',methods=["POST"])
def RunWorkPipeline():    #显示所有员工信息
    workpipeline=WorkPipeline()
    try:
        
        
        json_dict=request.get_json()
        # imgs_base64=json_dict["imgs_base64"]
        workpipeline.addpipelinetask( parsetask)\
        .addpipelinetask(imgrecttask)\
        .addpipelinetask(imgdetecttask)\
        .addpipelinetask(sentencecorrecttask)\
        .addpipelinetask(sentencejudgetask)\
        .addpipelinetask(packinfotesttask)
        

        workpipeline.runpipeline(json_dict,{
            "question_answer":json_dict["question_answer"]
        })
    
        print("anstext:",workpipeline.pass_context)
        return jsonify(
            {
                "workstate":workpipeline.pass_context["workstate"],
                **workpipeline.pass_context
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