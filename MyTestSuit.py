import unittest
import MyTestCase
import sellerShip


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(sellerShip.Test("test_shipGoods")) # 卖家发货
    suite.addTest(MyTestCase.Test("test_pay"))  # 买家下单
    # suite.addTest(MyTestCase.Test("test_adv"))  # 测试图谱
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())