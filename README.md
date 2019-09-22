**前言**

    因为Eolinker还是存在不足，有的功能无法满足需求，如参数化。
    所以就自己用python编写脚本。用的工具是vscode，框架python+unittest+htmlTestRunner。

**一、目录结构**

    setting     存放配置的文件夹:
        constant.py 以字典的形式来储存常量（相当于Eolinker中的测试环境）
        dbSetting.json  存放数据库配置
    
    report：
        输出报告的文件夹
    
    util    存放工具类的文件夹:
        excel.py
        Excel工具类，主要用于把数据输出为Excel保存起来
       
    MyTestCase.py:
        测试用例集（可以直接执行）
        
    MyTestSuit.py:
        可以根据需求从MutipleApiTest.py选择需要测试的用例
        如：suite.addTest(MultipleApiTest.Test('test_pay'))

**二、知识点**

    1、第三方库：
        ①unittest		单元测试框架
        ②requests		用于发送请求的
        ③json			用于解析json
        ④xlwt			用于Excel写入操作
    
    2、第三方库安装：
        cmd输入pip install xxx	（xxx为库名）
    
    3、自定义类
    
**ps:造数据常用**
    
    将MultipleApiTest中的方法添加到SingleApiTest的testSuite即可，
    并且要在MultipleApiTest中修改相关的user_id和token
    
    买家下单    test_pay
        下单的数目修改循环次数即可
        
    卖家发货    test_shipGoods
        执行会将待发货的数据遍历，每次最多可以发货10单（其他地方限制了）
    
    发布商品    test_ReleaseGoods
        发布商品的数量修改循环次数即可
