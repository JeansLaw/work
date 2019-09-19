import requests
import json

class HttpUtil():
    def postJson(self,url,data,headers):
        '''
        :param url: 完整的url
        :param data: 请求参数
        :param headers: 请求头
        :return:
        '''
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        return json.loads(res.text)

    def getJson(self,url,params=None):
        res=requests.get(url,params)
        return json.loads(res.text)