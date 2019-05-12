import logging
import os
import sys

from lhwill.settings import DEBUG

logger = logging.getLogger(__name__)

'''TODO'''
class log(object):

    def __init__(self, bals):
        self.bals = bals
        pass

    def get_module(self):
        bals = self.bals

        def main_module_name():
            mod = sys.modules['__main__']
            file = getattr(mod, '__file__', None)
            return file and os.path.splitext(os.path.basename(file))[0]

        def modname(fvars):
            try:
                file, name = fvars.get('__file__'), fvars.get('__name__')
                if file is None or name is None:
                    return None

                if name == '__main__':
                    name = main_module_name()
                return name
            except:
                return '请设置globals()方法'

        return modname(bals)

    def i(self, *args):
        print('Log[\'' + self.get_module() + '\'] :', *args)
        logger.info('Log[\'' + self.get_module() + '\'] :', *args)
        pass

    def e(self, *args):
        print('Log[\'' + self.get_module() + '\'] :', *args)
        logger.error('Log[\'' + self.get_module() + '\'] :', *args)
        pass

    pass


def i(bals, *args):
    log(bals).i(*args)
