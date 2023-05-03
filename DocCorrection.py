from doccorrection.model import DocGeoNet
from doccorrection.seg import U2NETP

import torch
import torch.nn as nn
import torch.nn.functional as F
# import skimage.io as io

import numpy as np
import cv2
import os
from PIL import Image



class Net(nn.Module):
    def __init__(self, opt):
        super(Net, self).__init__()
        self.msk = U2NETP(3, 1)
        self.DocTr = DocGeoNet()

    def forward(self, x):
        msk, _1,_2,_3,_4,_5,_6 = self.msk(x)
        msk = (msk > 0.5).float()
        x = msk * x

        _, _, bm = self.DocTr(x)
        bm = (2 * (bm / 255.) - 1) * 0.99

        return bm

def reload_rec_model(model, path=""):
    if not bool(path):
        return model
    else:
        model_dict = model.state_dict()
        pretrained_dict = torch.load(path, map_location='cuda:0')
        print(len(pretrained_dict.keys()))
        pretrained_dict = {k[7:]: v for k, v in pretrained_dict.items() if k[7:] in model_dict}
        print(len(pretrained_dict.keys()))
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

        return model

def reload_seg_model(model, path=""):
    if not bool(path):
        return model
    else:
        model_dict = model.state_dict()
        pretrained_dict = torch.load(path, map_location='cuda:0')
        print(len(pretrained_dict.keys()))
        pretrained_dict = {k[6:]: v for k, v in pretrained_dict.items() if k[6:] in model_dict}
        print(len(pretrained_dict.keys()))
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

        return model

class DocCorrector:
    def __init__(self,
      rec_path='./trained_models/docrecmodel/DocGeoNet.pth',seg_path="./trained_models/docrecmodel/preprocess.pth"):
      self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
      self.scmodel=Net(None).to(device=self.device)
      print("loading DocCorrector.............")
      reload_rec_model(self.scmodel.DocTr,rec_path)
      reload_seg_model(self.scmodel.msk,seg_path)
      print("loading DocCorrector complete")
      for param in self.scmodel.parameters():
        param.grad = None
      self.scmodel.eval()
      
      pass
    def rectify(self,img):
        # im_ori = np.array(img)
        im_ori = np.array(img)[:, :, :3]/255
        h, w, _ = im_ori.shape
        # h, w = im_ori.shape
        im = cv2.resize(im_ori, (256, 256))
        im = im.transpose(2, 0, 1)
        im = torch.from_numpy(im).float().unsqueeze(0)
        with torch.no_grad():
            bm = self.scmodel(im.cuda())
            bm = bm.cpu()

        # save rectified image
        bm0 = cv2.resize(bm[0, 0].numpy(), (w, h))  # x flow
        bm1 = cv2.resize(bm[0, 1].numpy(), (w, h))  # y flow
        bm0 = cv2.blur(bm0, (3, 3))
        bm1 = cv2.blur(bm1, (3, 3))
        lbl = torch.from_numpy(np.stack([bm0, bm1], axis=2)).unsqueeze(0)  # h * w * 2
        out = F.grid_sample(torch.from_numpy(im_ori).permute(2, 0, 1).unsqueeze(0).float(), lbl, align_corners=True)
        final=((out[0] * 255).permute(1, 2, 0).numpy())[:,:,::-1].astype(np.uint8)
        # cv2.imwrite(save_path + name + '_rec' + '.png', )
        return final
    