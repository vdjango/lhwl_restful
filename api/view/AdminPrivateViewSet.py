'''
admin相关接口，仅可用于私有访问，一般不对外开放，用户可发现接口，但是没有读取权限
本接口需要特殊身份验证[基于管理的身份验证，基于普通用户的身份验证]
以下操作需要身份验证
[GET HEAD PATCH PUT POST DELETE OPTIONS]
'''
from django.utils.datetime_safe import datetime
from rest_framework.response import Response

from api import viewsets
from api.serializers import SerializersAdmin
from api.util.ImportGoodsutils import ImportGoodsmodel
from api.util.UnzipFileutils import xzipfile
from managestage.models import ImportFile, ImportGoods


class ImportGoodsViewSet(viewsets.AdminMethodViewSet):
    '''
    https://github.com/simple-uploader/vue-uploader

    文件上传后端适配

    POST 上传文件

    POST /api/v2/admin/importgoods/

    PUT 文件上传完成后组合分片 [将组合后的文件添加到ImportGoods Model]

    > PUT /api/v2/admin/importgoods/

    > DATA:

    >     {

    >         filename: 文件名

    >         identifier: 每个文件的唯一标示

    >     }

    > 更多请参考 ImportFile 模型字段，皆可传入


    '''
    queryset = ImportFile.objects.filter()
    serializer_class = SerializersAdmin.ImportGoodsFileSerializer
    filter_fields = (
        'filename',
        'relativePath',
        'identifier',
        'totalSize',
        'currentChunkSize',
        'chunkSize',
        'totalChunks',
        'chunkNumber'
    )

    def put(self, request, *args, **kwargs):
        '''
        文件上传完成后组合分片
        将组合后的文件添加到ImportGoods Model
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        import os
        import time
        from lhwill import settings

        time = time.mktime(datetime.now().timetuple())

        orm_object = self.get_object_filter().order_by('chunkNumber')
        orm_file_path = []
        orm_path = '{}{}{}/'.format(settings.BASE_DIR, '/media/import_success/', int(time))

        for i in orm_object:
            orm_file_path.append({
                'id': i.chunkNumber,
                'path': i.file.path,
                'relativePath': i.relativePath
            })
            pass

        if not os.path.exists(orm_path):
            os.makedirs(orm_path)
            pass

        with open('{}{}'.format(orm_path, orm_file_path[0]['relativePath']),
                  'wb') as target_file:
            for file in orm_file_path:
                if os.path.exists(file['path']):
                    source_file = open(file['path'], 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                    print(file['path'])
                    os.remove(file['path'])
                pass
            pass

        orm_object.delete()

        ImportGoods.objects.create(
            file='import_success/{}/{}'.format(int(time), orm_file_path[0]['relativePath']),
            unix=int(time),
            name=orm_file_path[0]['relativePath']
        )

        return Response({
            'success': 'success',
            'orm_file_path': orm_file_path
        })
        pass

    pass


class ImportWareAppViewSet(viewsets.AdminMethodViewSet):
    '''
    将分片组合的压缩包导入到数据库

    PATCH 导入商品

    > PATCH /api/v2/admin/importgoodsset/{ID}/

    > DATA:

    >     {

    >         type: 'import'

    >     }

    > PATCH请求参数附带type: 'import'，将会解压压缩包，然后导入商品到数据库，如果没有附带，将是update操作
    '''
    queryset = ImportGoods.objects.filter()
    serializer_class = SerializersAdmin.ImportGoodsSerializer

    # 返回解压缩包路径
    #
    path_out = None

    def unzip(self):
        instance = self.get_object()
        xzip = xzipfile(instance.file.path)
        uzip = xzip.Unzip()
        self.path_out = xzip.pathOut
        xzip.close()
        return uzip
        pass

    def import_goods(self):
        import_goods = ImportGoodsmodel(self.kwargs[self.lookup_field], self.path_out)
        _import, _mess_ = import_goods.introduction()
        return _import, _mess_
        pass

    def update(self, request, *args, **kwargs):
        print('request.data', kwargs)
        try:
            if 'import' in request.data['type']:
                _unzip, _mess_ = self.unzip()
                if not _unzip:
                    context = {
                        'status': 'error',
                        'message': '解压失败了',
                    }
                    status = 415
                    return Response(context, status=status)

                _import, _mess_ = self.import_goods()
                if not _import:
                    context = {
                        'status': 'error',
                        'message': _mess_,
                    }
                    status = 415
                    return Response(context, status=status)

                context = {
                    'status': 'success',
                    'message': _mess_
                }
                status = 200

                return Response(context, status=status)
                pass
        except KeyError:
            pass

        return super(ImportWareAppViewSet, self).update(request, *args, **kwargs)

    pass
