import util.jerrySql as mysql
import os

filepath=os.path.abspath('..')
path=os.path.join(filepath,r"setting\dbSetting2.json")

sqlUtil=mysql.sqlUtil()
sqlUtil.settingPath(path)
sql="INSERT INTO user (`username`, `password`) VALUES ('admin', '123456')"
# sql="UPDATE `user` SET `username`='123' WHERE (`username`='sss')"
sqlUtil.excute(sql)
result=sqlUtil.query("SELECT * FROM user")
for item in result:
    print(item)
