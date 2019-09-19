import unittest
import time
import requests
import json
import setting.constant as constant

baseUrl = constant.env["url"]
user_id = constant.env["user"]["961366"]["user_id"]
token = constant.env["user"]["961366"]["token"]
store_id = constant.env["user"]["961370"]["user_id"]
seller_token = constant.env["user"]["961370"]["token"]
seller_user_id = constant.env["user"]["961370"]["user_id"]
title = ""

class Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("begin...")
    
    @classmethod
    def tearDown(self):
        print("end...")

    # 卖家发货
    def test_shipGoods(self):
        # 卖家待发货订单
        url=baseUrl+"/index.php?c=store"
        data={
            "json":[
                {
                    "status":20,
                    "keyword":"",
                    "token":seller_token,
                    "cmd":"6501",
                    "store_id":seller_user_id,
                    "page":1
                }
            ]
        }
        headers=constant.env["headers"]

        toStr=str(data)
        print("卖家待发货订单url:"+url+",request data:"+toStr.replace("\'","\""))
        
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        j=json.loads(res.text)
        js_6501=j["6501"]

        code=str(js_6501["statusCode"])
        print("data有"+str(len(js_6501["data"]))+"条数据")
        self.assertEqual("0",code,str(js_6501["errorMsg"]))

        for i in range(len(js_6501["data"])):
            # 卖家发货
            data={
                "json":[
                    {
                        "token":seller_token,
                        "order_id":js_6501["data"][i]["order_id"],
                        "invoice_proof":"",
                        "user_id":seller_user_id,
                        "cmd":"6503",
                        "store_id":seller_user_id,
                        "invoice_code":"kuaijiesudi",
                        "invoice_no":str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
                    }
                ]
            }
            headers=constant.env["headers"]

            toStr=str(data)
            print("卖家第"+str(i+1)+"次发货url:"+url+",request data:"+toStr.replace("\'","\""))
            
            res=requests.post(url=url,data=json.dumps(data),headers=headers)
            j=json.loads(res.text)
            js=j["6503"]

            code=str(js["statusCode"])
            self.assertEqual("0",code,str(js["errorMsg"]))
            time.sleep(1)


if __name__=="__main__":
    unittest.main()