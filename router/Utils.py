import cv2

import base64
import numpy as np
import hashlib
def img2base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64,buffer
def base64toimg(base64code):
    image_bytes = base64.b64decode(base64code)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image,image_bytes
def bytes2hash(bytes_buffer):
    hasher = hashlib.md5()
    hasher.update(bytes_buffer)
    image_hash = hasher.hexdigest()
    return image_hash
def multi_img2base64(imgs):
    imgs_base64=[]
    imgs_buffer=[]
    for img in imgs:
        img_base64,img_buffer= img2base64(img)
        imgs_base64.append(img_base64)
        imgs_buffer.append(img_buffer)
    return imgs_base64,imgs_buffer
def multi_base64toimg(imgs_base64):
    imgs=[]
    imgs_buffer=[]
    for img_base64 in imgs_base64:
        img,img_buffer= base64toimg(img_base64 )
        imgs.append(img)
        imgs_buffer.append(img_buffer)
    return imgs,imgs_buffer
def multi_bytes2hash(imgs_buffer):
    return [bytes2hash(img_buffer) for img_buffer in imgs_buffer]

