import os
import codecs
import random

from datetime import datetime
from lhwill import settings
from django.utils import timezone

def TIMEDATES():
    return timezone.now()


def buildFileName(filename):
    dt = datetime.now()
    name, ext = os.path.splitext(filename)
    return "%s" % (dt.strftime("%Y-%m-%d-%M-%H-%S-{0}{1}".format(random.randint(1, 999999), ext)))

def picupload(url, filename):
    '''

    :param request:
    :param form:  验证表单
    :param username:
    :return:
    '''

    name = buildFileName(filename.name)
    dest = os.path.join(settings.MEDIA_ROOT, url, name)

    print('dest', dest)
    if os.path.exists(dest):
        os.remove(dest)

    f = codecs.open(dest, "wb")
    for chunk in filename.chunks():
        f.write(chunk)

    f.flush()
    f.close()

    return dest, name


def copyimage(purl, surl):
    import shutil
    print(purl)
    shutil.copy(purl, surl)

    pass
