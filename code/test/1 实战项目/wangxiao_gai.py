import json
import time
import requests
import redis
from openpyxl import Workbook
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

redis_pool = redis.ConnectionPool(password='root' ,host='localhost',
            port=6379, db=0,decode_responses=True)
wb = Workbook()

class WangXiao:
    def __init__(self):
        self.cookies = {
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
        self.headers = {
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

        self.file_name = 'wangxiao.html'
        self.main_url = 'https://ks.wangxiao.cn/'
        self.t = ThreadPoolExecutor(max_workers=20)
        self.red = redis.Redis(connection_pool=redis_pool)
        self.index = ['A','B','C','D','E','F','F','G','H']
        self.ws = wb.active
        self.title1 = []
        self.title2 = []
        
        self.title = ''
        self.position = ''
        
    def download_main_html(self):
        with open(self.file_name, 'w',encoding='utf-8') as f:
            response = requests.get(self.main_url, headers=self.headers)
            f.write(response.text)
    
    def read_main_html(self):
        with open(self.file_name,'r',encoding='utf-8') as f:
            html = f.read()
            selector = etree.HTML(html)
            
            ul = selector.xpath('//ul[@class="first-title"]/li')
            for i,li in enumerate(ul):
                # . 表示当前节点
                # .. 表示父节点
                self.title1 = li.xpath('./p/span/text()')
                self.title2 = li.xpath('./div/a/text()')
                title2_url = li.xpath('./div/a/@href')

                info = {
                        'title1':self.title1[i],
                        'title2':'',
                        'url':''
                    }
                for j,url in enumerate(title2_url):
                    listEveryday_url = self.main_url + 'practice/listEveryday?' + url.split('?')[1]
                    info['title2'] = self.title2[j]
                    info['url'] = listEveryday_url
                    
                    str = info['title1'] + '-%*' + info['title2']+'-%*'+info['url']
                    self.t.submit(self.run_add_url,str)
                break
    
    def download_datails_html(self):
        with open('details.html','w',encoding='utf-8') as f:
            for i in self.red.sscan_iter('info'):
                datails_url = i.split('-%*')[2]
                response = requests.get(datails_url, headers=self.headers)
                selector = etree.HTML(response.text)
                paper = selector.xpath('//div[@class="test-panel"]/div')
                if paper:
                    # print(paper)
                    f.write(response.text)
                    self.title = i.split('-%*')[0]
                    self.position = i.split('-%*')[1]
                else:
                    print('没有找到')
                    continue
                break
    def read_details_html(self):
        with open('details.html','r',encoding='utf-8') as f:
            html = f.read()
            selector = etree.HTML(html)
            paper = selector.xpath('//div[@class="test-panel"]/div')
            
            for div in paper:
                url = div.xpath('./ul/li[4]/a/@href')[0]
                url = url.split('?')[1]
                practice_type = url.split('&')[0]
                sign = url.split('&')[1]
                subsign = url.split('&')[2]
                day = url.split('&')[3]
                print(practice_type,sign,subsign,day)
                break
            # https://ks.wangxiao.cn/practice/listQuestions
            
        data ={
            'practiceType':practice_type.split('=')[1],
            'sign':sign.split('=')[1],
            'subsign':subsign.split('=')[1],
            'day':day.split('=')[1]
        }

        response = requests.post(url='https://ks.wangxiao.cn/practice/listQuestions',headers=self.headers,cookies=self.cookies,json=data).json()
        for i in response['Data']:
            for question in i['questions']:
                self.t.submit(self.run_add_json,json.dumps(question,ensure_ascii=False))
    
    def read_pawer(self):
        self.ws.title = '试卷题目'
        # 类别 职位 题目 选项A 选项B 选项C 选项D 选项E 选项F 选项G 选项H 答案
        self.ws.append(['类别','职位','题目','选项A','选项B','选项C','选项D','选项E','选项F','选项G','选项H','答案'])

        for i in self.red.sscan_iter('question'):
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
            
            question_data = json.loads(i)
            question['题目'] = question_data['content']
            anwer = ''
            for number,option in enumerate(question_data['options']):
                question['选项'+self.index[number]] = option['content']
                if option['isRight'] == 1:
                    anwer = anwer + self.index[number]
                    question['答案'] = anwer
            
            question['类别'] = self.title
            question['职位'] = self.position
            
            question_value = question.values()
            # print(question_value)
            self.ws.append(list(question_value))
        wb.save('wangxiao.xlsx')

    def run_add_url(self,str):
        self.red.sadd('info',str)
    def run_add_json(self,str):
        self.red.sadd('question',str)
        
if __name__ == '__main__':
    start = time.time()
    wx = WangXiao()
    
    wx.download_main_html()
    wx.read_main_html()
    wx.download_datails_html()
    wx.read_details_html()
    
    # 确保线程全部执行完毕
    wx.t.shutdown()
    
    wx.read_pawer()
    
    end = time.time()
    print('耗时',end-start)