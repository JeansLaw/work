import hashlib
import os


class ReadFile():
    def getFileList(self, dir, Filelist):
        if os.path.isfile(dir):
            Filelist.append([os.path.basename(dir), dir])
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.getFileList(newDir, Filelist)
        return Filelist

    def getImgList(self, fileList):
        imgList = []
        imgBaseUrl = "https://test-1252710231.cos.ap-guangzhou.myqcloud.com/"
        for e in fileList:
            m = hashlib.md5()
            m.update(str(e[0]).encode("utf-8"))
            fileName = m.hexdigest()
            imgUrl = imgBaseUrl + fileName + ".jpg"
            imgList.append([e[0], imgUrl])

        return imgList

    def renameFile(self, path):
        '''
        将文件夹下所有文件从"原文件名"重命名为"父路径 原文件名"

        :param path: 文件夹路径
        :return:
        '''
        fileList = self.getFileList(path, [])
        print(fileList)

        for e in fileList:
            dir = os.path.abspath(os.path.dirname(e[1]))
            fileName = os.path.basename(e[1])
            dirName = os.path.basename(dir)

            oldName = dir + "\\" + fileName
            newName = dir + "\\" + dirName + " " + fileName
            print("old:" + oldName, "new:" + newName)
            os.rename(oldName, newName)
