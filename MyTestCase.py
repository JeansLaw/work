import json
import os
import re
import time
import unittest
import requests

from setting import constant
from util import File, Tecent
from util import myHttp, excel, jerrySql

# 用户数据
baseUrl = constant.env["url"]
user_id = constant.env["user"]["961371"]["user_id"]
user_name = constant.env["user"]["961371"]["user_name"]
token = constant.env["user"]["961371"]["token"]
phone_number = constant.env["user"]["961371"]["phone_number"]
store_id = constant.env["user"]["961370"]["user_id"]
seller_token = constant.env["user"]["961370"]["token"]
seller_user_id = constant.env["user"]["961370"]["user_id"]
headers = constant.env["headers"]
title = ""

# 数据库
httpUtil = myHttp.HttpUtil()
sqlUtil = jerrySql.sqlUtil()
pwd = os.path.abspath("./setting")
filePath = os.path.join(pwd, "dbSetting.json")
sqlUtil.settingPath(filePath)

# 创建excel sheet
exc = excel.ExcelUtil()
exc.setWorkBook()
exc.setSheet("sheet1")
getcwd = os.path.abspath(os.path.dirname("."))
path = os.path.join(getcwd + r"\report",
                    "demo_{0}.xls".format(str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))))
# print('\033[1;33m{0}\033[3;31m'.format("文件输出路径：") + path)
print('\033[0m')
exc.writeXls(path, ["cmd", "测试用例", "StatusCode", "响应时间", "Msg", "Url", "data"])

tecentUtil = Tecent.Util()


class Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("begin...")

    @classmethod
    def tearDown(self):
        exc.writeXls(path, [""])
        print('\033[1;33m{0}\033[3;31m'.format("文件输出路径：") + path)
        print("end...")

    def test_adv(self):
        # 遍历文件生成数组
        fileUtil = File.ReadFile()
        testpath = r"D:\work"
        fileList = fileUtil.getFileList(testpath, [])

        # 上传文件到cos
        for e in fileList:
            tecentUtil.uploadImg(e[1], e[0])

        # 生成测试数据
        imgList = tecentUtil.getImgList(fileList)

        # 循环请求
        for e in imgList:
            print(e)
            imgUrl = e[1]
            testCase = e[0]
            url = baseUrl + "/index.php?c=goods"
            cmd = "11552"
            data = {
                "json": [{
                    "cmd": cmd,
                    "type": 0,
                    "image_url": imgUrl,
                    "user_id": user_id,
                    "user_name": user_name,
                    "token": token
                }]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\"").replace(r"\\", "\\"))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            exc.writeXls(path, [cmd, e[0], js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"").replace(r"\\", "\\")])
            if js["statusCode"] != 0:
                break

            # 上传图片至图谱获取返回结果
            try:
                tpUrl = "http://test-api2.ppwang.com:8800/index.php?c=test&m=requestTupuCheakTest&type=0&imageUrl=" + e[
                    1]
                res = requests.get(tpUrl)
                r = str((res.text)[:-5])

                js = json.loads(r)
                js = json.loads(js["json"])

                tpData = []
                if js["56a8645b0c800bff40990cf1"]["statistic"] != None:
                    tpData.append(["广告识别", js["56a8645b0c800bff40990cf1"]["statistic"]])
                if js["5acb135cc40c6772b10ec73a"]["statistic"] != None:
                    tpData.append(["暴恐识别", js["5acb135cc40c6772b10ec73a"]["statistic"]])
                if js["54bcfc6c329af61034f7c2fc"]["statistic"] != None:
                    tpData.append(["色情识别", js["54bcfc6c329af61034f7c2fc"]["statistic"]])

                exc.writeXls(path, ["。", e[0], str(res.status_code), "。", "。", str(tpUrl), str(tpData)])
                exc.writeXls(path, [""])
                time.sleep(1)

            except Exception as e:
                print(e)

    def test_pay(self):
        sql = "SELECT goods_id FROM ecm_goods WHERE store_id={0} AND if_show=1;".format(seller_user_id)
        goodsResult = sqlUtil.query(sql)
        # for i in range(len(result)):
        #     print(result[i][0])
        #     if i ==len(result)-1:
        #         break
        for i in range(len(goodsResult)):
            testCase = "获取spec_id"
            url = baseUrl + "/index.php?c=member"
            cmd = "1001"
            print("result:" + str(goodsResult[i]))
            goods_id = goodsResult[i][0]
            data = {
                "json": [
                    {
                        "goods_id": goods_id,
                        "user_id": user_id,
                        "cmd": cmd,
                        "token": token
                    }
                ]
            }
            # headers = constant.env["headers"]
            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            spec_id = js["data"]["spec"][0]["spec_id"]

            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"")])

            testCase = "添加进货车"
            url = baseUrl + "/index.php?c=member"
            cmd = "5301"

            data = {
                "json": [
                    {
                        "is_together": 0,
                        "cmd": cmd,
                        "token": token,
                        "activity_type": "0",
                        "goods_source_type": 3,
                        "goods_id": goods_id,
                        "module_source": "店铺首页",
                        "activity_type_id": "0",
                        "spec": [
                            {
                                "quantity": "2",
                                "spec_id": spec_id
                            }
                        ],
                        "goods_source_related_id": "0",
                        "user_id": user_id
                    }
                ]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]

            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"")])

            testCase = "获取addr_id和shipping_id"
            url = baseUrl + "/index.php?c=member"
            cmd = "5400"
            data = {
                "json": [
                    {
                        "goods_id": [
                            goods_id
                        ],
                        "user_id": user_id,
                        "cmd": "5400",
                        "token": token
                    }
                ]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            addr_id = js["data"]["address"]["addr_id"]
            shipping_id=js["data"]["shipping"][str(seller_user_id)][0]["shipping_id"]
            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,str(data).replace("\'", "\"")])



            testCase = "提交订单"
            url = baseUrl + "/index.php?c=member"
            cmd = "5401"
            data = {
                "json": [
                    {
                        "goods_id": [
                            goods_id
                        ],
                        "is_together": 0,
                        "no_reason_refund": 0,
                        "addr_id": addr_id,
                        "cmd": cmd,
                        "token": token,
                        "user_id": user_id,
                        "shipping": [
                            {
                                "message": "",
                                "shipping_id": shipping_id,
                                "shippingName": "快递",
                                "shippingPrice": 0.01,
                                "store_id": seller_user_id
                            }
                        ]
                    }
                ]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            order_id_5401 = js["data"][0]
            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"")])

            testCase = "发起支付"
            url = baseUrl + "/index.php?c=member"
            cmd = "5403"
            data = {
                "json": [
                    {
                        "order_id": [
                            order_id_5401
                        ],
                        "payment_code": "pipipay",
                        "cmd": cmd,
                        "token": token,
                        "user_id": user_id
                    }
                ]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            order_id_5403 = js["data"]["order_id"]
            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"")])

            testCase = "确认支付"
            time.sleep(3)
            sql = "SELECT out_msg FROM ecm_sms_record WHERE phone_number={0} ORDER BY id DESC LIMIT 1;".format(
                phone_number)
            print(sql)
            rows = sqlUtil.query(sql)
            check_code = ""
            for row in rows:
                string = row[0]
                result = re.compile(r'\d+').findall(string)  # 查找数字
                check_code = result[0]
            url = baseUrl + "/index.php?c=store"
            cmd = "11003"
            data = {
                "json":
                    [
                        {
                            "order_id": order_id_5403,
                            "check_code": check_code,
                            "cmd": "11003",
                            "check_type": "buypayorder",
                            "token": token,
                            "user_id": user_id
                        }
                    ]
            }
            # headers = constant.env["headers"]

            print(cmd + testCase + "url:" + url, ",request data:" + str(data).replace("\'", "\""))

            j = httpUtil.postJson(url, data, headers)
            js = j[cmd]
            code = str(js["statusCode"])

            exc.writeXls(path, [cmd, testCase, js["statusCode"], js["qtime"], js["errorMsg"], url,
                                str(data).replace("\'", "\"")])
            self.assertEqual("0", code, str(js["errorMsg"]))
            exc.writeXls(path, [""])


if __name__ == "__main__":
    unittest.main()
