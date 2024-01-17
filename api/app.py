# coding:utf-8
import time
import hashlib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
# import pyperclip
import json

import requests
import uuid
import time
import string
import random


# 创建随机UA
def get_user_agent():
    tmp1 = random.randrange(90, 120)
    tmp2 = random.randrange(5200, 5500)
    tmp3 = random.randrange(90, 180)
    tmp_version = str(tmp1) + ".0." + str(tmp2) + "." + str(tmp3)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + \
        tmp_version + ' Safari/537.36'
    # print(ua)
    return ua


# md5加密字符串
def get_hash(str):
    obj = hashlib.md5()
    obj.update(str.encode("utf-8"))
    result = obj.hexdigest()
    return result


# 仿制captcha_sign
def get_sign(begin_str):
    salts = [{'alg': 'md5', 'salt': '6ov9AjGrStwPh+Dy9CSYcJ+QesOX'},
             {'alg': 'md5', 'salt': ''},
             {'alg': 'md5', 'salt': 'tpn69xYajl9QCoDcBquNmW'},
             {'alg': 'md5', 'salt': 'IEFNmRWeu6bbHQG'},
             {'alg': 'md5', 'salt': 'DPmuDzz1EDfKSWvj4QrkawjOaSuVBR/Wpb8AuERPCJH/pwDn9R78'},
             {'alg': 'md5', 'salt': 'nfGllh2kOXm/2KqpHHAeAa9X5B4GjGL4tZ'},
             {'alg': 'md5', 'salt': '7PaOcGq2REG9IGlMvdz2H1DhS1bO9uQY/fAUw2y766iQ+l'},
             {'alg': 'md5', 'salt': 'BLs1AD/VKU/6M23HzJcna'},
             {'alg': 'md5', 'salt': '6lS6PzMP'},
             {'alg': 'md5', 'salt': 'iO36B4qMPNAqjt3JAR8KGddkY'},
             ]

    # print("Salts：" + str(salts))
    hex_str = begin_str
    for salt in salts:
        hex_str = get_hash(hex_str + salt["salt"])
    # print("Sign：", hex_str)
    return hex_str


# 安全验证-登录
def login_init(client_id, device_id, email, user_agent):
    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    payload = {
        "client_id": client_id,
        "action": "POST:/v1/auth/signin",
        "device_id": device_id,
        "captcha_token": "",
        "meta": {"email": email}
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return json.loads(response.text)


# 登录
def get_login(username, password, client_id, device_id, user_agent, captcha_token):
    url = "https://user.mypikpak.com/v1/auth/signin"

    payload = {
        "username": username,
        "password": password,
        "client_id": client_id
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-captcha-token": captcha_token,
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return json.loads(response.text)


# 获取验证CODE
def get_authorize(client_id, device_id, access_token, user_agent):
    url = "https://user.mypikpak.com/v1/user/authorize"

    payload = {
        "client_id": client_id,
        "state": "ignored",
        "scope": "user+pan+offline",
        "response_type": "code",
        "redirect_uri": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf"
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "Authorization": "Bearer " + access_token,
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return json.loads(response.text)


# 获取真正access_token
def get_token(code, client_id, user_agent):
    url = "https://user.mypikpak.com/v1/auth/token"

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id
    }
    headers = {
        "authority": "user.mypikpak.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/json",
        "origin": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": user_agent,
        "x-client-id": client_id,
        "x-protocol-version": "301",
        "x-sdk-version": "5.2.0",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return json.loads(response.text)


# 安全验证-领取奖励
def reward_init(device_id, captcha_token, captcha_sign, timestamp, aliyungf_tc, user_agent, client_id):
    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    payload = {
        "client_id": client_id,
        # "action": "POST:/vip/v1/activity/rewardVip",
        "action": "POST:/vip/v1/vip/info",
        "device_id": device_id,
        "captcha_token": captcha_token,
        "meta": {
            "captcha_sign": "1." + captcha_sign,
            "client_version": "1.4.6",
            "package_name": "mypikpak.com",
            "timestamp": timestamp
        }
    }
    headers = {
        "authority": "user.mypikpak.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/json",
        "cookie": "aliyungf_tc=" + aliyungf_tc,
        "origin": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": user_agent,
        "x-client-id": client_id,
        "x-protocol-version": "301",
        "x-sdk-version": "5.2.0",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return json.loads(response.text)



def get_vip_datas(user_agent,device_id,access_token,captcha_token):
    
    headers = {
        "User-Agent": user_agent,
        "X-Device-Id": device_id,
        "authorization": "Bearer " + access_token,
        "x-captcha-token": captcha_token,

        "Accept-Language": "zh",
        "Content-Type": "application/json; charset=utf-8",
        # "cookie": "aliyungf_tc=" + aliyungf_tc,
        # "Content-Length": "149",
        # "Host": "user.mypikpak.com",
  

        "Connection": "Keep-Alive",
        # "Accept-Encoding": "gzip"
    }
    # print(headers)
    dd = requests.get("https://api-drive.mypikpak.com/vip/v1/vip/info", headers=headers)
    # print(dd.json())
    return dd.json()


def inviteCode(access_token, captcha_token, device_id, user_agent):
        """
        eyJhbGciOiJSUzI1NiIsImtpZCI6ImJiZjUyNzc3LTMwMmUtNGZkMC04ZTRiLWY3ZjQ3ZGI4N2JjMCJ9.eyJpc3MiOiJodHRwczovL3VzZXIubXlwaWtwYWsuY29tIiwic3ViIjoiWmFkNWY5Qk50SHRMR2peFQ5dzdHTWRXdkVPS2EiLCJleHAiOjE3MDU0ODE2MzEsImlhdCI6MTcwNTQ3NDQzMSwiYXRfaGFzaCI6InIuTEExaDFMVUZFZTZJSGNhQ0NqMzZtQSIsInNjb3BlIjoidXNlciBwYW4gc3luYyBvZmZsaW5lIiwicHJvamVjdF9pZCI6IjJ3a3M1NmMzMWRjODBzeGXZKo0Sio7xENeLuWCABVexuujUtn_pNW_nOnAawzzPSojuErtk1b8ZXWbsqh4yjPzycfsAGDQnBZBRHm5GnsIblVBG5cj8VDyDR8ultW1YHm7VyvwEr2wxzw_M32DcuFlBUqFRRnK4QzevnzgPcv9xnxeeRi4-97_Ustj_HifAQKnfXozwcAuXf3naocP_CuutyrTh9PAGOLv3y8Ici3TF_HOi-3-_zMvpSAGvZjFNG_gnzaZVCXQEtlNHjOiGhnqIXVGql0An5ffZkOccDj2zZi-_Xalv-Rf957egd2Y3OHDRWjoYJtjnmvoy7Ig
        """
        # headers = {
        #     "authorization": f"Bearer {authorization}"
        # }

        headers = {
            'Host': 'api-drive.mypikpak.com',
            "User-Agent": user_agent,
            "X-Device-Id": device_id,
            "authorization": "Bearer " + access_token,
            "x-captcha-token": captcha_token,
            'country': 'CN',
            'accept-language': 'zh-CN',
            'x-peer-id': 'xid',
            'x-user-region': '2',
            'x-system-language': 'zh-CN',
            'x-alt-capability': '3',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.get('https://api-drive.mypikpak.com/vip/v1/activity/inviteCode', headers=headers)
        
        return response.json()["code"]

# 运行程序
def start(email, password):
    # 模拟设备基本配置
    client_id1 = "YUMx5nI8ZU8Ap8pm"
    client_id2 = "Ypcug64Odf8hwuKB"
    device_id = str(uuid.uuid4()).replace("-", "")
    user_agent = get_user_agent()
    # 开始模拟请求
    captcha_token = login_init(client_id1, device_id, email, user_agent)[
        "captcha_token"]

    login_data = get_login(email, password, client_id1,
                           device_id, user_agent, captcha_token)
    access_token = login_data["access_token"]
    code = get_authorize(client_id2, device_id,
                         access_token, user_agent)["code"]
    token = get_token(code, client_id2, user_agent)
    access_token = token['access_token']
    aliyungf_tc = str(uuid.uuid4()).replace("-", "") + \
        str(uuid.uuid4()).replace("-", "")
    timestamp = "1694680977127"
    # timestamp = str(int(time.time()) * 1000)
    str1 = client_id2 + "1.4.6mypikpak.com" + device_id + timestamp
    captcha_sign = get_sign(str1)
    captcha_token = reward_init(device_id, captcha_token, captcha_sign, timestamp, aliyungf_tc, user_agent, client_id2)[
        'captcha_token']
    # data.vipItem[0].surplus_day
    surplus_day = get_vip_datas(user_agent,device_id,access_token,captcha_token)['data']['vipItem'][0]['surplus_day']
    
    inviteCode_data = inviteCode(access_token, captcha_token, device_id, user_agent)
    
    return (surplus_day,inviteCode_data)


def get_data(kind_id="505018174505029"):
    headers = {
        'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDU0Njk5ODUsIm5iZiI6MTcwNTQ2OTk4NSwiZXhwIjoxNzA2MDc0Nzg1LCJzaWQiOjUwNTAwMjcxNDU5MTMwMSwidWlkIjo1MDUwMDI3MTQ1OTEzMDIsIm5hbWUiOiJweXRob25cdTVjMGZcdTVlOTcifQ.I8uxtQmfXC7_CG6LZ-EhF6819izd-pzPsC1fCeHbjVs',
        'dnt': '1',
        'origin': 'http://goofish.pro',

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        'idx': '1',
        'count': '0',
        'size': '25',
        'kind_id': kind_id,# 5天vip
        'sale_status': '1',
    }
    response = requests.get(
        'https://api.goofish.pro/api/kam/storage/pager', params=params, headers=headers)

    # print(response.json())
    data_json = response.json()
    if "data" not in data_json:
        return []

    data_list = data_json["data"]
    if len(data_list)==0:
        return []
 
    return data_list

def post_vip(invite_code='37066433',times_invite=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    tem_times = 0
    while True:
        try:
            print(f"第{tem_times}次邀请\n")
            for index in range(1, 16):
                data = {
                    'orderInput': '更新会员',
                    'fun_items': f'{index}',
                    'invite_code': invite_code,
                    'invite_times': '[object HTMLInputElement]',
                }

                response = requests.post('https://mbpikpak.vercel.app/submit-order', headers=headers, data=data).json()

                print(response)
                if index == 15 and "邀请成功" in response['message']:
                    tem_times +=1
            
            if tem_times==times_invite:
                return True
        except Exception as e:
            print(e)


def post_vip2(invite_code='37066433',fun_items=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
   

    try:
       

        data = {
            'orderInput': '更新会员',
            'fun_items': f'{fun_items}',
            'invite_code': invite_code,
            'invite_times': '[object HTMLInputElement]',
        }

        response = requests.post('https://mbpikpak.vercel.app/submit-order', headers=headers, data=data).json()

        print(response)
        # if index == 15 and "邀请成功" in response['message']:
        #     tem_times +=1
        return response
    
    except Exception as e:
        print(e)

            
def main():
    kind_id5 = "505018174505029" # 5天
    kind_id30 = "505021378220101" # 30天
    kind_id100 = "505021763530821" # 100天

    data_kind = {
        "505018174505029":5,
        "505021378220101": 30,
        "505021763530821":100,
    }
    kind_id_datas = kind_id30

    data_list = get_data(kind_id=kind_id_datas)
    print(data_list)
    # pikpak_data = ["5sjfyjc0kn@zipcatfish.com","mobai2024"]
    for data in data_list:
        

        email = data['card_no']
        password = data['pwd_decrypt']
        print( f"正在使用账号：{email} 密码：{password}")

        surplus_day, inviteCode_data = start(email, password)
        print(f"您的会员剩余天数是：{surplus_day},邀请码:{inviteCode_data}")
        surplus_day_mast = data_kind[kind_id_datas]
        
        if int(surplus_day) < surplus_day_mast:
            print("您的会员即将到期，请及时续费")
            times_invite = int((surplus_day_mast-int(surplus_day))/2)
            print(f"您需要邀请{times_invite}位好友")

            # for index in range(times_invite+1):
            post_vip(invite_code=inviteCode_data,times_invite=times_invite)




def main2(card_no,pwd_decrypt,kind_id):
    # kind_id5 = "505018174505029" # 5天
    # kind_id30 = "505021378220101" # 30天
    # kind_id100 = "505021763530821" # 100天

    data_kind = {
        "505018174505029":5,
        "505021378220101": 30,
        "505021763530821":100,
    }
    kind_id_datas = kind_id

    data_list = [{
        "card_no":card_no,
        "pwd_decrypt":pwd_decrypt
    }]
    print(data_list)
    # pikpak_data = ["5sjfyjc0kn@zipcatfish.com","mobai2024"]
    for data in data_list:
        

        email = data['card_no']
        password = data['pwd_decrypt']
        print( f"正在使用账号：{email} 密码：{password}")

        surplus_day, inviteCode_data = start(email, password)
        print(f"您的会员剩余天数是：{surplus_day},邀请码:{inviteCode_data}")
        surplus_day_mast = data_kind[kind_id_datas]
        
        
        if int(surplus_day) < surplus_day_mast:
            print("您的会员即将到期，请及时续费")
            times_invite = int((surplus_day_mast-int(surplus_day))/2)
            print(f"您需要邀请{times_invite}位好友")
            return {"msg":f"剩余天数：{surplus_day},邀请码:{inviteCode_data},需要次数:{times_invite}","inviteCode":inviteCode_data,"times_invite":times_invite}
        else:
            return {"msg":f"剩余天数：{surplus_day},邀请码:{inviteCode_data}","inviteCode":inviteCode_data,"times_invite":0}
        #     for index in range(times_invite+1):
        #         post_vip2(invite_code=inviteCode_data,times_invite=times_invite)



app = Flask(__name__)
# 解决跨域问题，非常重要
CORS(app, supports_credentials=True)




@app.route('/submit-order', methods=['POST', "GET"])
def submit_order():
    order_info = request.form['orderInput']
    fun_items = request.form['fun_items']
    invite_times = request.form['invite_times']
    invite_code = request.form['invite_code']
    print(fun_items)
    # 在实际应用中，这里可以将订单信息存储到数据库或进行其他处理
    # generate = PK.post_data(invite_code="49682958", times=1)
    # 复制结果到剪贴板
    # pyperclip.copy(order_info)
    # data = "\n".join(mail_list)

    # return app.response_class(generate(), mimetype='application/json')

    return jsonify(message=f'订单已成功提交{fun_items}\n', order_info=order_info)


@app.route('/invite_now', methods=['POST', "GET"])
def invite_now():
    # order_info = request.form['orderInput']
    fun_items = request.form['fun_items']
    # invite_times = request.form['invite_times']
    invite_code = request.form['invite_code']

    
    # print(fun_items)
    # res_data = main_post(int(fun_items), invite_code)
    res_data = post_vip2(invite_code=invite_code, fun_items=fun_items)


    return jsonify(message=f'{str(res_data["message"])}\n')



@app.route('/get_vip_data', methods=['POST', "GET"])
def get_vip_data():
    # print(request.json)
    pwd_decrypt = request.json['pwd_decrypt']
    card_no = request.json['card_no']
    kind_id = request.json['kind_id']
    
    print(pwd_decrypt)

    res_data = main2(card_no,pwd_decrypt,kind_id)

    return jsonify(message=f'状态: {str(res_data["msg"])}\n',invite_code=res_data["inviteCode"],times_invite=res_data["times_invite"])

@app.route('/get_kami_data', methods=['POST', "GET"])
def get_kami_data():
    kind_id = request.json['kind_id']
    data_list = get_data(kind_id=kind_id)

    return data_list


path_d = os.path.dirname(os.path.realpath(__file__))
index_html = open(f'{path_d}/templates/index.html',
                  'r', encoding='utf-8').read()

# print(index_html)


@app.route('/', methods=['GET'])
def get_request():

    return index_html



# user_html = open(f'./templates/index.html', 'r', encoding='utf-8').read()

# # http://127.0.0.1:8088/api/get_user?user=墨白
# @app.route('/', methods=['GET'])
# def get_user():
#     return user_html


# if __name__ == '__main__':
#     app.run(port=8087, host='0.0.0.0', debug=False)

#     # main()
#     # post_vip("25129828",2)
    
