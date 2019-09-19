现有问题

    1
    https://test-1252710231.cos.ap-guangzhou.myqcloud.com/%E4%BA%8C%E7%BB%B4%E7%A0%811.jpg
    上传之后返回的信息↓↓↓
    "code\":14,\"message\":\"Download fail. response statusCode: 400
    域名为https://test-1252710231.cos.ap-guangzhou.myqcloud.com/的图片图谱那边都会下载失败
    
    2
    url="http://test-api2.ppwang.com:8800/index.php?c=test&m=requestTupuCheakTest&type=0&imageUrl=http://test-img1.ppwang.com/other/201909/17/5ccf14087707ee4dddd042c68df4b749.gif"
    # 访问
    res=requests.get(url)
    r=str((res.text)[:-5])
    #读取返回信息
    js=json.loads(r)
    js=json.loads(js["json"])
    print(str(js).replace("\'","\""))
    
    
    返回信息：
    {"code": 14, "message": "Invalid file format: gif", "nonce": "0.722195647061155", "timestamp": 1568787472301}
    gif格式图片无法识别