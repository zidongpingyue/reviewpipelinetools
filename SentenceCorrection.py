from transformers import BertTokenizer, BertForMaskedLM
import torch
import operator
import Config
import re
class SentenceCorrector:
    def __init__(self,path=Config.stnrec_model_path):

      self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
      self.pattern=Config.split_pattern
      
      print("loading sentence correction")
      self.tokenizer = BertTokenizer.from_pretrained(path)
      self.model = BertForMaskedLM.from_pretrained(path)
      print("loading sentence correction completed")
      self.model.to(self.device)
      
      for param in self.model.parameters():
        param.grad = None
      
      self.model.eval()
      pass
    @staticmethod
    def get_errors(corrected_text, origin_text):
          sub_details = []
          for i, ori_char in enumerate(origin_text):
              if ori_char in [' ', '“', '”', '‘', '’', '琊', '\n', '…', '—', '擤',' ']:
                  # add unk word
                  corrected_text = corrected_text[:i] + ori_char + corrected_text[i:]
                  continue
              if i >= len(corrected_text):
                  continue
              if ori_char != corrected_text[i]:
                  if ori_char.lower() == corrected_text[i]:
                      # pass english upper char
                      corrected_text = corrected_text[:i] + ori_char + corrected_text[i + 1:]
                      continue
                  sub_details.append((ori_char, corrected_text[i], i, i + 1))
          sub_details = sorted(sub_details, key=operator.itemgetter(2))
          return corrected_text, sub_details
    def sentencecorrect(self,longsentence):
        
      result = [(m.group(), m.start()) for m in re.finditer(self.pattern, longsentence)]
      longsentences = [i[0] for i in result]
      with torch.no_grad():
          tokens=self.tokenizer(longsentences, padding=True, return_tensors='pt').to(self.device)
          outputs = self.model(**tokens)
      result = []
      for ids, text in zip(outputs.logits, longsentences):
          if text.isspace():
              continue
        #   _text = self.tokenizer.decode(torch.argmax(ids, dim=-1), skip_special_tokens=True).replace(' ', '')
          _text = self.tokenizer.decode(torch.argmax(ids, dim=-1), skip_special_tokens=True).replace(' ', '')
          corrected_text = _text[:len(text)]
          corrected_text, details = SentenceCorrector.get_errors(corrected_text, text)
          print(text, ' => ', corrected_text, details)
          result.append((corrected_text, details))
      return result
