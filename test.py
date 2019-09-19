import json

import requests

url="http://test-api2.ppwang.com:8800/index.php?c=test&m=requestTupuCheakTest&type=0&imageUrl=https://test-1252710231.cos.ap-guangzhou.myqcloud.com/f9cc69a51b6463cce40919bbec4519c0"

res=requests.get(url)
r=str((res.text)[:-5])

js=json.loads(r)
print(js)
js=json.loads(js["json"])

# print(str(js).replace("\'","\""))

tpData=[]
if js["56a8645b0c800bff40990cf1"]["statistic"] != None:
    tpData.append(["广告识别", js["56a8645b0c800bff40990cf1"]["statistic"]])
if js["5acb135cc40c6772b10ec73a"]["statistic"] != None:
    tpData.append(["暴恐识别", js["5acb135cc40c6772b10ec73a"]["statistic"]])
if js["54bcfc6c329af61034f7c2fc"]["statistic"] != None:
    tpData.append(["色情识别", js["54bcfc6c329af61034f7c2fc"]["statistic"]])

strTpData = "";
for data in tpData:
    strTpData = strTpData+str(data[0])+str(data[1]) + "\n"

print(strTpData)
