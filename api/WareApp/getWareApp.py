import json

from django.http import HttpResponse

from app import models
from managestage.utli.wrapper import _GET


@_GET
def getWare(request):
	'''
	获取商品
	:param request:
	:return:
	'''
	id = request.GET.get('id')
	try:
		ware = models.WareApp.objects.get(id=id)
		try:
			image = models.images.objects.filter(key=ware)[:1].get().image
		except:
			image = '/static/images/ware/404.png'
			pass
		wareapp = {
			'id': ware.id,
			'name': ware.name,
			'money': float(ware.money),
			'image': image
		}

		content = {
			'state': 'success',
			'data': wareapp,
			'code': '200'
		}
	except:
		content = {
			'state': 'error',
			'error': '商品不存在',
			'code': '404'
		}

	return HttpResponse(json.dumps(content))
	pass