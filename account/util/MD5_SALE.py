# -------------------------------------------
# Python简单密码加密程序
# 随机生成4位salt，与原始密码组合，通过md5加密
# Author : Lrg
# -------------------------------------------
# encoding = utf-8
from random import Random
from lhwill.settings import SECRET_KEY
from hashlib import md5


class MD5():
    def __init__(self, password,  salt=None):
        self.AULE = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        self.salt = self.set_salt(length=16, salt=salt)
        self.md5 = self.md5_salt(password, self.salt)
        print('md5', md5)

    # 获取由4位随机大小写字母、数字组成的salt值
    def set_salt(self, length=4, salt=None):
        chars = SECRET_KEY
        print('AULE', self.AULE)
        chars = list('{}{}'.format(
            self.AULE,
            chars
        ))
        chars.sort()
        chars = "".join(chars)

        len_chars = len(chars) - 1
        random = Random()
        if not salt:
            salt = ''
            for i in range(length):
                salt += chars[random.randint(0, len_chars)]

        return salt.encode("utf8")

    def md5_salt(self, password, salt):
        password += salt
        m = md5()
        m.update(password)
        return m.hexdigest()

    def get_salt(self):
        return self.salt






