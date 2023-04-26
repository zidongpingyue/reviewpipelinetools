from sentence_transformers import SentenceTransformer
from scipy import spatial
from sentence_transformers import CrossEncoder
import re
import Config
import torch
class TextJudger:
    def __init__(self):
      self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
      self.pattern=r"[^，。、：\n]+"
      print("loading SentenceTransformer..............")
      self.smodel = SentenceTransformer(Config.smodel_path,device=self.device)
      print("loading CrossEncoder.................") 
      self.cmodel = CrossEncoder(Config.cmodel_path,device=self.device)
      print("loading complete.....................")
      self.   scoremap=[0,1,0.5] 
      pass
    #获取topk相似的句子
    def GetTopKSim (self,longsentence,shortsentence,topk=4):
        result = [(m.group(), m.start()) for m in re.finditer(self.pattern, longsentence)]
        longsentences = [i[0] for i in result]
        # print(longsentences)
        longembeddings = self.smodel.encode(longsentences)
        shortembedding = self.smodel.encode(shortsentence)
        data=[]

        for sentence, embedding in zip(result, longembeddings):
            if len(sentence)<=1:
                continue
            cos_sim = 1 - spatial.distance.cosine(shortembedding, embedding)
            el=spatial.distance.euclidean(shortembedding, embedding)
            #输出 (句子,余弦相似度,向量距离,句子在原文的位置)
            data.append((sentence[0],cos_sim,el,sentence[1]))
        #以余弦相似度排序
        data=sorted(data,key=lambda x: x[1], reverse=True)
        retdata=[]
        for i in range(topk):
            retdata.append(data[i])
        return retdata
    
    #获取匹配的最大分数:准确匹配(浮点数)
    def GetAdvancedMatchScores( self,topk_sentences,short_sentence):
        scores = self.cmodel.predict([(i[0],short_sentence) for i in topk_sentences])
        labels = [self.scoremap[score_max] for score_max in scores.argmax(axis=1)]
        #label,index,long
        finalresult=[(label,sentence[3],len(sentence[0])) for label,sentence in zip(labels,topk_sentences)]
        return finalresult
    #获取最终分数
    def CalculateLabelScore(self,labels):
        entails=[]
        score=0
        for i in labels:
            if(i[0]==1):
                score=1
                entails.append(i)
        return score,entails
    def CalculateScore(self,long_sentence,real_short_sentence):
            topk_sentences=self.GetTopKSim(long_sentence,real_short_sentence)
            topk_labels=self.GetAdvancedMatchScores(topk_sentences,real_short_sentence)
            final_score=self.CalculateLabelScore(topk_labels) 
            return final_score