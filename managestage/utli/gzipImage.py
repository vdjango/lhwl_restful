import os

from PIL import Image
from lhwill.settings import BASE_DIR

def compressImage(srcPath):
    for filename in os.listdir(srcPath):
        srcFile = os.path.join(srcPath, filename)
        print(srcFile)

        # 如果是文件就处理
        if os.path.isfile(srcFile):
            image = Image.open(srcFile)  # 通过cp.picture 获得图像
            image = image.convert('RGB')
            width = image.width
            height = image.height
            ratio = 0.5
            if width > 2000:
                image.thumbnail((width*ratio, height*ratio), Image.ANTIALIAS)  # 生成缩略图
            else:
                image.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图

            image.save(str(srcFile), 'JPEG')  # 保存到原路径
        # 如果是文件夹就递归
        if os.path.isdir(srcFile):
            compressImage(srcFile)



