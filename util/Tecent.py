# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
import hashlib
from urllib import parse

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = ''  # 替换为用户的 secretId
secret_key = ''  # 替换为用户的 secretKey
region = 'ap-guangzhou'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

class Util():
    def __md5(self, fileName):
        m = hashlib.md5()
        m.update(str(fileName).encode("utf-8"))
        return m.hexdigest()

    def uploadImg(self, filePath, fileName):
        with open(filePath, 'rb') as fp:
            fileName = self.__md5(fileName)
            client.put_object(
                Bucket='test-125',
                Body=fp,
                Key=fileName + ".jpg",
                StorageClass='STANDARD',
                EnableMD5=False
            )

    def getImgList(self, fileList):
        imgList = []
        imgBaseUrl = "https://test-1252710231.cos.ap-guangzhou.myqcloud.com/"
        for e in fileList:
            fileName = self.__md5(str(e[0]))
            imgUrl = imgBaseUrl + fileName + ".jpg"
            imgList.append([e[0], imgUrl])

        return imgList
