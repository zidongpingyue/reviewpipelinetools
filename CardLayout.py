import cv2 
import numpy as np
from PIL import ImageFont,ImageDraw,Image


class CardGennerator:
    def __init__(self, img_size):
      self.size=img_size
      self.images=[]
      self.front=ImageFont.truetype("./fronts/simsun.ttc",40,encoding="utf-8")

      pass
 
    def Generateimg(self):
      img=np.zeros((self.size[1],self.size[0],3),np.uint8) #设置背景
      img.fill(255)
      return img
    def answer_box(self,img,title,beginpos,size_tuple,y_box_offset=5):
      x_,y_=beginpos
      
      offsetx,offsety=size_tuple
      
      # cv2.putText(img,title,(x_+15,y_+30+15), cv2.FONT_HERSHEY_SIMPLEX, 
      #              1, (0,0,0), 1, cv2.LINE_AA)

      img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
      draw = ImageDraw.Draw(img_pil)
      draw.text((x_+25,y_+25),text=title,font=self.front,fill=(0,0,0))
      img = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)
      # print("debug img.....") 
      # cv2_imshow(img)
      cv2.rectangle(img, (x_,y_+y_box_offset), (x_+offsetx,y_+y_box_offset+offsety), (0,0,255), thickness=6)
      # self.img=img
      return img
    def Simplelayout(self,layout):
      current_page=-1
      current_img=None
      for line in layout:
        pages=line[0]
        title=line[2]
        margin=line[1]
        part=0
        for page in pages:
          pageid,begin_line,line_length=page
          if current_page!=pageid:
            if current_img is not None:
              self.images.append(current_img)
            current_page=pageid
            current_img=self.Generateimg()
          
          t_title=f"{title}、"
          if part!=0:
            t_title=f"{title}、续{part}"
          current_img=self.answer_box(current_img,t_title,(margin[0],begin_line),(1000-(margin[0]+margin[1]),line_length))
      
          part+=1
      if current_img is not None:
        self.images.append(current_img)
      return self.images



class ConfigParser:
    def __init__(self):
      
      self.pages=[]
      self.margin=(60,60)#left right
      self.wordrect=(25,25)
      self.paperrect=(1000,1414)
      self.vertpad=90
      self.vertendpad=80
      pass
    @staticmethod
    def split_page(page_lines:int,current_page:int,current_line:int,lines_num:int,interval=2,begin_offset=60,min_page_lines=200):
      rest_num=page_lines-current_line

      if rest_num<min_page_lines:
          pages_num=int(lines_num)//int(page_lines+interval)
          remainder_num=int(lines_num)%int(page_lines+interval)
          remainder=[(current_page+pages_num+1,begin_offset+0,int(remainder_num))]
          # [(pageid,begin_line,line_length).....],after_pageid,after_linenum
          return [(i+current_page,begin_offset+0,int(page_lines)) for i in range(int(pages_num))]+remainder,int(current_page+pages_num+1),int(remainder_num+interval)
      elif rest_num>=lines_num:
          return [(current_page,int(current_line)+begin_offset,int(lines_num))],int(current_page),int(current_line+lines_num+interval)
      
      else :
          lines_num_left=lines_num-rest_num
          head=[(current_page,current_line+begin_offset,int(rest_num))]
          pages_num=int(lines_num_left)//int(page_lines+interval)
          remainder_num=int(lines_num_left)%int(page_lines+interval)
          reaminder_real_lines=max(int(remainder_num),min_page_lines)
          remainder=[(current_page+pages_num+1,begin_offset+0,reaminder_real_lines)]
          # [(pageid,begin_line,line_length).....],after_pageid,after_linenum
          return head+[(i+current_page,begin_offset+0,int(page_lines)) for i in range(int(pages_num))]+remainder,int(current_page+pages_num+1),int(reaminder_real_lines+interval)



    def GenerateLayout(self,paper_rect,config_dict):
      questions=config_dict["questions"] 
      layout_=[]
      w,h=paper_rect
      current_line=0
      current_page=0
      for question in questions:
        type_=question["type"]
        order_=question["order"]
        maxwords_=question["maxwords"]
        # line_offset=0
        # print(order_)
        if type_=="subjective":
          # beginpos_=(current_line,self.margin)
          line_words=int((self.paperrect[0]-(self.margin[0]+self.margin[1]))/self.wordrect[0])
          height_lines=int(maxwords_/line_words)
          print(height_lines)
          height_offset=self.wordrect[1]*height_lines
          pages,current_page,current_line=ConfigParser.split_page(page_lines=self.paperrect[1]-self.vertendpad*2,current_page=current_page,current_line=current_line,lines_num=height_offset,interval=self.vertpad
                                                                  ,begin_offset=self.vertendpad)
          print("liter:",order_,pages,current_page,current_line)
          layout_.append((pages,self.margin,order_))
      return layout_

     

