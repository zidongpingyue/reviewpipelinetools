from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
import cv2

'''
1、通用文字识别,图像数据base64编码后大小不得超过10M
2、appid、apiSecret、apiKey请到讯飞开放平台控制台获取并填写到此demo中
3、支持中英文,支持手写和印刷文字。
4、在倾斜文字上效果有提升，同时支持部分生僻字的识别
'''

APPId = "af159fc9"  # 控制台获取
APISecret = "Y2IzMWQxYWFjYzY3NmRiNDAzMDllZWQ5"  # 控制台获取
APIKey = "5f1f3559a63c70adfceb0acc74dbf2b0"  # 控制台获取
# file_path='newpaper_word.png'


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


def Character_recognition(zip_image):

    _,img_b=cv2.imencode('.png',zip_image)
    imageBytes=img_b.tobytes()
    # with open(file_path, "rb") as f:
    #     imageBytes = f.read()

    # print(len(str(base64.b64encode(imageBytes))))
    url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'

    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "sf8e6aca1": {
                "category": "ch_en_public_cloud",
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            # "sf8e6aca1_data_1": {
            #     "encoding": "png",
            #     "image": str(base64.b64encode(imageBytes), 'UTF-8'),
            #     "status": 3
            # },
            "sf8e6aca1_data_1": {
                "encoding": "jpg",
                "image": str(base64.b64encode(imageBytes), 'UTF-8'),
                "status": 3
            }
        }
    }

    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    # print(request_url)
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    # print(response)
    # print(response.content)

    # print("resp=>" + response.content.decode())
    tempResult = json.loads(response.content.decode())

    finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
    finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    # print("text字段Base64解码后=>" + finalResult)

    # with open('s.json','w',encoding='utf-8') as f:
    #     f.write(finalResult)
    return finalResult

# 以字典返回识别结果，对文本行进行排序
def result(zip_image,area_list):
    data=json.loads(Character_recognition(zip_image))
    answers={}
    flag=1
    for area_index in range(len(area_list)):
        area=area_list[area_index]
        parms=area.reshape(8,-1)
        for page in data['pages']:
            for line in page['lines']:
                # print(line)
                if line['exception']==0 and 0<line['conf']<1:                   
                    coord=line['coord']
                    y_mean=sum(y['y'] for y in coord)/4
                    for point in coord:
                        if(not isInSide(*parms,point['x'],point['y'])):
                            flag=0
                    if flag==0:
                        flag=1
                        continue
                    else:
                        if(str(area_index+1) not in answers.keys()):
                            answers[str(area_index+1)]=[[y_mean],[]]
                        else:
                            answers[str(area_index+1)][0].append(y_mean)
                        for word in line['words']:
                            content=word['content']
                            answers[str(area_index+1)][1].append(content)
                            # print(content)

    for key in answers.keys():
        ls=answers[f'{key}']
        answers[f'{key}']=list(zip(ls[0],ls[1]))

    for key in answers.keys():
        answers[f'{key}'].sort(key=lambda item:item[0])
    
    for key in answers.keys():
        string=''
        for item in answers[f'{key}']:
                string+=item[1]
        answers[f'{key}']=string
    
    new_answers=[answer[1] for answer in answers.items()]
                        
    # print(answers)
    return new_answers

# 计算(x1,y1)(x,y)、(x2,y2)(x,y)向量的叉乘
def GetCross(x1,y1,x2,y2,x,y):
    a=(x2-x1,y2-y1)
    b=(x-x1,y-y1)
    return a[0]*b[1]-a[1]*b[0]

# 判断(x,y)是否在矩形内部
def isInSide(x1,y1,x2,y2,x3,y3,x4,y4,x,y):
    return GetCross(x1,y1,x2,y2,x,y)*GetCross(x3,y3,x4,y4,x,y)>=0 and GetCross(x2,y2,x3,y3,x,y)*GetCross(x4,y4,x1,y1,x,y)>=0

