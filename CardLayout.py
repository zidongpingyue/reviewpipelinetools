import cv2 
import numpy as np


'''
读取layout生成n页答题卡
'''
class CardGennerator:
    def __init__(self, img_size):
      self.size=img_size
      self.images=[]
      
      pass
 
    def Generateimg(self):
      img=np.zeros((self.size[1],self.size[0],3),np.uint8) #设置背景
      img.fill(255)
      return img
    def answer_box(self,img,num,beginpos,size_tuple,y_box_offset=5):
      x_,y_=beginpos
      offsetx,offsety=size_tuple
      
      # cv2.putText(img, "Question:"+str(num)+" End",(x_,y_+y_box_offset+offsety+30), cv2.FONT_HERSHEY_SIMPLEX, 
      #              1, (0,0,0), 1, cv2.LINE_AA)
      cv2.putText(img, "Question:"+str(num)+"",(x_,y_+30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,0), 1, cv2.LINE_AA)
      cv2.rectangle(img, (x_,y_+y_box_offset), (x_+offsetx,y_+y_box_offset+offsety), (0,0,0), thickness=2)
      # return self.img
    def Simplelayout(self,layout):
      current_page=-1
      current_img=None
      for line in layout:
        pages=line[0]
        title=line[2]
        margin=line[1]
        for page in pages:
          pageid,begin_line,line_length=page
          if current_page!=pageid:
            if current_img is not None:
              self.images.append(current_img)
            current_page=pageid
            current_img=self.Generateimg()
          self.answer_box(current_img,title,(margin[0],begin_line),(1000-(margin[0]+margin[1]),line_length))
      if current_img is not None:
        self.images.append(current_img)
      return self.images
"""
读取layout与imgs
"""
class ImageParser:
    def __init__(self,img_size):
      self.img_size=img_size
      # self.layout=layout
      pass
    def Parse(self,images,layout):
      current_page=-1
      current_img=None
      crop_imgs=[]
      for line in layout:
        pages=line[0]
        title=line[2]
        margin=line[1]
        for page in pages:
          pageid,begin_line,line_length=page
          if current_page!=pageid:
            current_page=pageid
            current_img=images[current_page]
          # print("page_id:",pageid)
          begin_point=(margin[0],begin_line)
          end_point=(1000-(margin[1]),line_length+begin_line+1)
          if current_img is not None:
            crop = current_img[begin_point[1]:min(end_point[1],self.img_size[1]),begin_point[0]:min(end_point[0],self.img_size[0])]# [ymin:ymax,xmin:xmax]
            # print(current_img.shape)
            crop_imgs.append((crop,title,pageid))
      return crop_imgs


"""
dict_={
  "questions":[
            {
          "order":1,
          "type":"subjective",
          "maxwords":500
      },
      {
          "order":2,
          "type":"subjective",
          "maxwords":600
      },
      {
          "order":3,
          "type":"subjective",
          "maxwords":500
      },
      {
          "order":4,
          "type":"subjective",
          "maxwords":1000
      }
   
  ]
}
转换为layout
"""
class ConfigParser:
    def __init__(self, config_dict):
      self.questions=config_dict["questions"]
      self.pages=[]
      self.margin=(65,10)#left right
      self.wordrect=(25,25)
      self.paperrect=(1000,1414)
      self.vertpad=40
      pass
    @staticmethod
    def split_page(page_lines:int,current_page:int,current_line:int,lines_num:int,interval=2):
      rest_num=page_lines-current_line
      if rest_num>=lines_num:
          return [(current_page,int(current_line),int(lines_num))],int(current_page),int(current_line+lines_num+interval)
      else :
          lines_num_left=lines_num-rest_num
          head=[(current_page,current_line,int(rest_num))]
          pages_num=int(lines_num_left)//int(page_lines+interval)
          remainder_num=int(lines_num_left)%int(page_lines+interval)
          remainder=[(current_page+pages_num+1,0,int(remainder_num))]
          # [(pageid,begin_line,line_length).....],after_pageid,after_linenum
          return head+[(i+current_page,0,int(page_lines)) for i in range(int(pages_num))]+remainder,int(current_page+pages_num+1),int(remainder_num+interval)
    def GenerateLayout(self,paper_rect):
      layout_=[]
      w,h=paper_rect
      current_line=0
      current_page=0
      for question in self.questions:
        type_=question["type"]
        order_=question["order"]
        maxwords_=question["maxwords"]
        # line_offset=0
        # print(order_)
        if type_=="subjective":
          # beginpos_=(current_line,self.margin)
          line_words=int((self.paperrect[0]-(self.margin[0]+self.margin[1]))/self.wordrect[0])
          height_lines=int(maxwords_/line_words)
          # print(height_lines)
          height_offset=self.wordrect[1]*height_lines
          pages,current_page,current_line=ConfigParser.split_page(page_lines=self.paperrect[1],current_page=current_page,current_line=current_line,lines_num=height_offset,interval=self.vertpad)
          # print("liter:",order_,pages,current_page,current_line)
          layout_.append((pages,self.margin,order_))
      return layout_
