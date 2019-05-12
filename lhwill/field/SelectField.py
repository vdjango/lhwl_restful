from django.db import models
import ast

from lhwill.util.log import log

logger = log(globals())

# 自定义一个ListFiled,继承与TextField这个类
class SelectField(models.TextField):
    description = "just a listfiled"

    # 继承TextField
    def __init__(self, *args, **kwargs):
        super(SelectField, self).__init__(*args, **kwargs)

    # 读取数据库的时候调用这个方法
    def from_db_value(self, value, expression, conn, context):
        if not value:
            value = []
        if isinstance(value, list):
            logger.i('from_db_value', value)
            return value

        # 直接将字符串转换成python内置的list
        return ast.literal_eval(value)

    # 保存数据库的时候调用这个方法
    def get_prep_value(self, value):
        if not value:
            return value
        return str(value)
