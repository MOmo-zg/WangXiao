import json
import requests
import redis
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from openpyxl import Workbook

redis_pool = redis.ConnectionPool(password='root' ,host='localhost',
            port=6379, db=0,decode_responses=True)
red = redis.Redis(connection_pool=redis_pool)
wb = Workbook()
ws = wb.active

t = ThreadPoolExecutor(10)

cookies = {
    'userInfo': '%7B%22userName%22%3A%22pc_675520740%22%2C%22token%22%3A%222de828be-94ed-49a8-8d0e-733a332eea37%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22191****2117%22%2C%22sign%22%3Anull%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D%22%2C%22passwordCookies%22%3A%22Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D%22%7D',
    'token': '2de828be-94ed-49a8-8d0e-733a332eea37',
    'UserCookieName': 'pc_675520740',
    'OldUsername2': 'bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D',
    'OldUsername': 'bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D',
    'OldPassword': 'Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D',
    'UserCookieName_': 'pc_675520740',
    'OldUsername2_': 'bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D',
    'OldUsername_': 'bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D',
    'OldPassword_': 'Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': 'userInfo=%7B%22userName%22%3A%22pc_675520740%22%2C%22token%22%3A%222de828be-94ed-49a8-8d0e-733a332eea37%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22191****2117%22%2C%22sign%22%3Anull%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D%22%2C%22passwordCookies%22%3A%22Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D%22%7D; token=2de828be-94ed-49a8-8d0e-733a332eea37; UserCookieName=pc_675520740; OldUsername2=bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D; OldUsername=bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D; OldPassword=Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D; UserCookieName_=pc_675520740; OldUsername2_=bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D; OldUsername_=bDKZrL1Gn9FW3%2BVuWFsGVw%3D%3D; OldPassword_=Vhlel%2FKjlML0kxe9%2BRAd5A%3D%3D',
    'DNT': '1',
    'Origin': 'https://ks.wangxiao.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ks.wangxiao.cn/practice/getQuestion?practiceType=1&sign=jzs1&subsign=5166078fbf1eed222fe9&day=20240705',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

file_name = 'wangxiao.html'
main_url = 'https://ks.wangxiao.cn/'

# 获取首页
# with open(file_name, 'w',encoding='utf-8') as f:
#     response = requests.get(url, headers=headers)
#     f.write(response.text)

# def add_url(url):
#     red.sadd('wangxiao',url)

# with open(file_name,'r',encoding='utf-8') as f:
#     html = f.read()
#     selector = etree.HTML(html)
    
#     ul = selector.xpath('//ul[@class="first-title"]/li')
#     for li in ul:
#         # . 表示当前节点
#         # .. 表示父节点
#         title1 = li.xpath('./p/span/text()')[0]
#         title2 = li.xpath('./div/a/text()')
#         print(title2)
#         title2_url = li.xpath('./div/a/@href')
#         print(title2)
#         print(title2_url)
#         # https://ks.wangxiao.cn/practice/listEveryday?sign=jzs1
#         # https://ks.wangxiao.cn/TestPaper/list?sign=jzs1
        
#         for url in title2_url:
#             listEveryday_url = main_url + 'practice/listEveryday?' + url.split('?')[1]
#             t.submit(add_url,listEveryday_url)
#         break

# with open('details.html','w',encoding='utf-8') as f:
#     for i in red.sscan_iter('wangxiao'):
#         response = requests.get(i, headers=headers)
#         selector = etree.HTML(response.text)
#         paper = selector.xpath('//div[@class="test-panel"]/div')
#         if paper:
#             print(paper)
#             f.write(response.text)
            # for div in paper:
            #     url = div.xpath('./ul/li[4]/a/@href')[0]
            #     url = url.split('?')[1]
            #     practice_type = url.split('&')[0]
            #     sign = url.split('&')[1]
            #     subsign = url.split('&')[2]
            #     day = url.split('&')[3]
            #     print(practice_type,sign,subsign,day)
                
            #     data ={
            #         'practiceType':practice_type.split('=')[1],
            #         'sign':sign.split('=')[1],
            #         'subsign':subsign.split('=')[1],
            #         'day':day.split('=')[1]
            #     }
                
            #     response = requests.post(url='https://ks.wangxiao.cn/practice/listQuestions',headers=headers,cookies=cookies,json=data)
                
            #     break
        # else:
        #     print('没有找到')
        #     continue
        # break

# with open('details.html','r',encoding='utf-8') as f:
#     html = f.read()
#     selector = etree.HTML(html)
#     paper = selector.xpath('//div[@class="test-panel"]/div')
    
#     for div in paper:
#         url = div.xpath('./ul/li[4]/a/@href')[0]
#         url = url.split('?')[1]
#         practice_type = url.split('&')[0]
#         sign = url.split('&')[1]
#         subsign = url.split('&')[2]
#         day = url.split('&')[3]
#         print(practice_type,sign,subsign,day)
#         break
#     # https://ks.wangxiao.cn/practice/listQuestions

# data ={
#     'practiceType':practice_type.split('=')[1],
#     'sign':sign.split('=')[1],
#     'subsign':subsign.split('=')[1],
#     'day':day.split('=')[1]
# }

# response = requests.post(url='https://ks.wangxiao.cn/practice/listQuestions',headers=headers,cookies=cookies,json=data).json()

# def add_json(str):
#     red.sadd('question',str)

# for i in response['Data']:
#     for question in i['questions']:
#         t.submit(add_json,json.dumps(question,ensure_ascii=False))

def add_data(data):
    red.sadd('question_data',json.dumps(data,ensure_ascii=False))

content_list = []
option_content_list = []
is_right = []

ws.title = '试卷题目'
# 类别 职位 题目 选项A 选项B 选项C 选项D 选项E 选项F 选项G 选项H 答案
ws.append(['类别','职位','题目','选项A','选项B','选项C','选项D','选项E','选项F','选项G','选项H','答案'])

index = ['A','B','C','D','E','F','F','G','H']

for i in red.sscan_iter('question'):
    question = {
    '类别':'',
    '职位':'',
    '题目':'',
    '选项A':'',
    '选项B':'',
    '选项C':'',
    '选项D':'',
    '选项E':'',
    '选项F':'',
    '选项G':'',
    '选项H':'',
    '答案':''
    }
    # pprint(json.loads(i))
    question_data = json.loads(i)
    question['题目'] = question_data['content']
    anwer = ''
    for number,option in enumerate(question_data['options']):
        question['选项'+index[number]] = option['content']
        if option['isRight'] == 1:
            anwer = anwer + index[number]
            question['答案'] = anwer
    
    # t.submit(add_data,question)
    # pprint(question)
    question_value = question.values()
    print(question_value)
    ws.append(list(question_value))
wb.save('wangxiao.xlsx')

# pprint(question)
# t.shutdown()









