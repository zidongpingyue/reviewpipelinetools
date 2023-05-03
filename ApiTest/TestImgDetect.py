import http.client
import json
import cv2
import os,sys
sys.path.append("D:/Grocery/hw/AutoReviewProject/")

from router.Utils import img2base64
import TestConfig
headers = {'Content-type': 'application/json'}
img=cv2.imread("./img_data/img_rec/IMG_20230426_192359_rec.png")
print("shape:",img.shape)
data = {"imgs_base64":[
    img2base64(img)[0]
    # Utils.img2base64(cv2.imread("../img_data/img_afterrec/IMG_20230426_192444_rec.png"))
]}
json_data = json.dumps(data)
apiname=f"/detectimg"
conn = http.client.HTTPConnection(f"{TestConfig.testhost}")
conn.request('POST', apiname, body=json_data, headers=headers)
response = conn.getresponse()
data = response.read()
json_data=json.loads(data)
print(json_data["answers_text"])
conn.close()