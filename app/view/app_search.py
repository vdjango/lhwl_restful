from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from app import models
from account.util.email import login_mail
from app.models import WareSetupPrefix
from lhwill import settings
from lhwill.util import log
from managestage.models import Setclassify
from managestage.utli import HttpUrl
from managestage.utli.wrapper import _GET, Web_Maintain


class search(object):
	def __init__(self, searchs, search_ok, lend, evp, evs, evj, evf, evq):
		self.searchs = searchs
		self.search_ok = search_ok
		self.lend = lend
		self.evp = self.getValue(evp)  # 品牌
		self.evs = self.getValue(evs)  # 类型
		self.evj = self.getValue(evj)  # 技术类型
		self.evf = self.getValue(evf)  # 使用场景
		self.evq = self.getValue(evq)  # 价钱
		pass

	def getValue(self, vstr):
		s = str(vstr).split('[.!@]')
		if len(s) > 1:
			return s[1]
		else:
			return ''
		pass

	def getOjbectsModels(self):
		searchs = self.searchs
		search_ok = self.search_ok
		lend = self.lend
		evp = self.evp  # 品牌
		evs = self.evs  # 类型
		evj = self.evj  # 技术类型
		evf = self.evf  # 使用场景
		evq = self.evq  # 价钱
		print(lend)

		Front, After = HttpUrl.UrlSection(lend, '/admin/list/')
		Wapp = None

		'''
		if searchs:
			Wapp = models.WareAppPrefix.objects.filter(
				Q(wareApp_key__name__contains=searchs)|
				Q(brands=evp)|
				Q(producttypes=evs)|
				Q(technologys=evj)|
				Q(scenes=evf)|
				Q(priceranges=evq)
			)[Front:After]
		'''

		if not evp and not evs and not evj and not evf and not evq:

			if searchs and search_ok:
				print(search_ok)
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter()[Front:After]
			pass
		elif evp and not evs and not evj and not evf and not evq:
			print('品牌------', evp)
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp
					)[Front:After]
			pass
		elif evp and evs and not evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						producttypes=evs
					)[Front:After]
			pass

		elif evp and evs and evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					producttypes=evs,
					technologys=evj,
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						producttypes=evs,
						technologys=evj,
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						producttypes=evs,
						technologys=evj,
					)[Front:After]
			pass

		elif evp and evs and evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					producttypes=evs,
					technologys=evj,
					scenes=evf,
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						producttypes=evs,
						technologys=evj,
						scenes=evf,
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						producttypes=evs,
						technologys=evj,
						scenes=evf,
					)[Front:After]
			pass

		elif evp and evs and evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					producttypes=evs,
					technologys=evj,
					scenes=evf,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						producttypes=evs,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						producttypes=evs,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and evs and evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					producttypes=evs,
					technologys=evj,
					scenes=evf,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						producttypes=evs,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						producttypes=evs,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and not evs and evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					scenes=evf,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						scenes=evf,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and not evs and not evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and not evs and not evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						priceranges=evq
					)[Front:After]
			pass

		elif evp and not evs and evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					scenes=evf,
					technologys=evj,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						scenes=evf,
						technologys=evj,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						scenes=evf,
						technologys=evj,
						priceranges=evq
					)[Front:After]
			pass

		elif evp and evs and not evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					scenes=evf,
					priceranges=evq,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						scenes=evf,
						priceranges=evq,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						scenes=evf,
						priceranges=evq,
						producttypes=evs
					)[Front:After]
			pass

		elif evp and evs and evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					technologys=evj,
					priceranges=evq,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						technologys=evj,
						priceranges=evq,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						technologys=evj,
						priceranges=evq,
						producttypes=evs
					)[Front:After]
			pass

		elif evp and not evs and not evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					scenes=evf,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						scenes=evf,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						scenes=evf,
						priceranges=evq
					)[Front:After]
			pass

		elif evp and not evs and not evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						priceranges=evq
					)[Front:After]
			pass

		elif evp and evs and not evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					producttypes=evs,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and evs and not evj and evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					producttypes=evs,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and evs and not evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					producttypes=evs,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						producttypes=evs,
						priceranges=evq
					)[Front:After]
			pass

		elif not evp and evs and not evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						producttypes=evs
					)[Front:After]
			pass

		elif not evp and evs and not evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						producttypes=evs
					)[Front:After]
			pass

		elif not evp and evs and evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					producttypes=evs,
					technologys=evj
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						producttypes=evs,
						technologys=evj
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						producttypes=evs,
						technologys=evj
					)[Front:After]
			pass

		elif not evp and evs and evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					producttypes=evs,
					technologys=evj
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						producttypes=evs,
						technologys=evj
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						producttypes=evs,
						technologys=evj
					)[Front:After]
			pass

		elif not evp and evs and not evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						producttypes=evs
					)[Front:After]
			pass

		elif not evp and not evs and not evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf
					)[Front:After]
			pass

		elif not evp and not evs and evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					technologys=evj
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						technologys=evj
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						technologys=evj
					)[Front:After]
			pass

		elif not evp and not evs and evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj
					)[Front:After]
			pass

		elif not evp and not evs and evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj,
						priceranges=evq
					)[Front:After]
			pass

		elif evp and evs and not evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					brands=evp,
					scenes=evf,
					producttypes=evs
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						brands=evp,
						scenes=evf,
						producttypes=evs
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						brands=evp,
						scenes=evf,
						producttypes=evs
					)[Front:After]
			pass

		elif not evp and evs and evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					producttypes=evs,
					priceranges=evq
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj,
						producttypes=evs,
						priceranges=evq
					)[Front:After]
			pass

		elif evp and not evs and not evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					scenes=evf,
					brands=evp
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						scenes=evf,
						brands=evp
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						scenes=evf,
						brands=evp
					)[Front:After]
			pass

		elif evp and not evs and evj and not evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					brands=evp
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						brands=evp
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj,
						brands=evp
					)[Front:After]
			pass

		elif evp and not evs and evj and not evf and evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					priceranges=evq,
					brands=evp
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						priceranges=evq,
						brands=evp
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj,
						priceranges=evq,
						brands=evp
					)[Front:After]
			pass

		elif evp and not evs and evj and evf and not evq:
			if searchs and search_ok:
				Wapp = models.WareAppPrefix.objects.filter(
					classifytheres__icontains=search_ok,
					wareApp_key__name__icontains=searchs,
					technologys=evj,
					brands=evp,
					scenes=evf
				)[Front:After]
			else:
				if search_ok:
					Wapp = models.WareAppPrefix.objects.filter(
						classifytheres__icontains=search_ok,
						technologys=evj,
						brands=evp,
						scenes=evf
					)[Front:After]
				else:
					Wapp = models.WareAppPrefix.objects.filter(
						technologys=evj,
						brands=evp,
						scenes=evf
					)[Front:After]
			pass
		else:
			Wapp = None

			pass

		print('None', Wapp)
		wareapp = []
		if Wapp:
			for i in Wapp:
				images_ware = i.wareApp_key.images_set.filter()
				try:
					images_ware = images_ware[1].image
				except:
					images_ware = None

				if i.wareApp_key.release:
					wareapp.append({
						'id': i.wareApp_key.id,
						'name': i.wareApp_key.name,
						'money': i.wareApp_key.money,
						'unix': i.wareApp_key.unix,
						'image': images_ware
					})
					pass
			pass
		return wareapp, Wapp
		pass

	pass



def app_Searchs(request, lend):
	from managestage.models import SearchStatistics

	searchs = request.GET.get('search')
	search_ok = request.GET.get('searback')

	evp = request.GET.get('evp')  # 品牌
	evs = request.GET.get('evs')  # 类型
	evj = request.GET.get('evj')  # 技术类型
	evf = request.GET.get('evf')  # 使用场景
	evq = request.GET.get('evq')  # 价钱

	classifications = models.Classification.objects.filter()  # 全部分类
	navigation_two = models.Navigation_Two.objects.filter()  # 子导航
	navigation = models.Navigation.objects.filter()  # 导航

	wareapp = search(searchs, search_ok, lend, evp, evs, evj, evf, evq)
	search_new, warePrefix = wareapp.getOjbectsModels()
	auth_search = False  # 搜索到结果为 True
	key = None

	if len(search_new) > 0 and classifications[0]:
		print('用户搜索到商品', warePrefix.filter()[:1].get())
		auth_search = True

		search_filter = warePrefix.filter()[:1].get()
		aaa = search_filter.classifythere_key
		print('aaa ------ ', aaa)

		key = models.Classification_There.objects.filter(id=search_filter.classifythere_key_id)[0]
		print('key-----------------', key)
		'''
		统计用户搜索关键字习惯
		'''
		if searchs:
			try:
				Statistics = SearchStatistics.objects.get(name__icontains=searchs)
				Statistics.number += 1
				Statistics.save()
			except:
				SearchStatistics(
					name=searchs,
					number=1
				).save()
		pass

	print('SEARCH ---- ', search_ok, search_new, key)
	if search_ok:
		keys = models.Classification_There.objects.filter(name=search_ok)
		print('name--------', keys[0].id)
		if keys:
			key = keys[0]
		pass
	else:
		if key:
			search_ok = key.name
		else:
			search_ok = models.Classification_There.objects.filter()[:1]
			if search_ok:
				search_ok = search_ok.get()
			else:
				search_ok = ''
				pass
		pass



	WarePrefix = models.WareSetupPrefix.objects.filter(key=key)

	log.i(globals(), WarePrefix)


	pricerange = models.PriceRange.objects.filter(key=WarePrefix.get(filter_id='4'))  # 价格范围
	producttype = models.ProductType.objects.filter(key=WarePrefix.get(filter_id='1')[:1].get())  # 产品类型
	technology = models.Technology.objects.filter(key=WarePrefix.get(filter_id='2')[:1].get())  # 技术类型
	scene = models.Scene.objects.filter(key=WarePrefix.get(filter_id='3')[:1].get())  # 使用场景
	brand = models.Brand.objects.filter(key=WarePrefix.get(filter_id='0')[:1].get())  # 品牌





	content = {
		'search_ok': search_ok,
		'search': searchs,
		'wareapp': search_new,
		'auth_search': auth_search,
		'brand': brand,
		'productType': producttype,
		'technology': technology,
		'scene': scene,
		'priceRange': pricerange,
		'Classifications': classifications,
		'navigation': navigation,
		'navigation_two': navigation_two
	}

	log.i(globals(), content)
	return render(request, 'defaule/app/search.html', content)



def app_Search(request, lend):
	from managestage.models import SearchStatistics

	search = request.GET.get('search')
	if not search:
		search = ''

	Newsearch = request.GET.get('searback')

	classify = models.Classification.objects.filter()  # 全部分类
	nav = models.Navigation.objects.filter()  # 导航
	navtwo = models.Navigation_Two.objects.filter()  # 子导航


	t1 = request.GET.get('t1')  # 品牌
	t2 = request.GET.get('t2')  # 类型
	t3 = request.GET.get('t3')  # 技术类型
	t4 = request.GET.get('t4')  # 使用场景
	t5 = request.GET.get('t5')  # 价钱

	if t1:
		t1 = str(t1).split('.')[1]  # 品牌
	else:
		t1 = ''
	if t2:
		t2 = str(t2).split('.')[1]  # 类型
	else:
		t2 = ''
	if t3:
		t3 = str(t3).split('.')[1]  # 技术类型
	else:
		t3 = ''
	if t4:
		t4 = str(t4).split('.')[1]  # 使用场景
	else:
		t4 = ''
	if t5:
		t5 = str(t5).split('.')[1]  # 价钱
	else:
		t5 = ''




	Qst = Q()

	Qst.connector = 'AND'
	Qst.children.append(('brand_key__name__icontains', t1))
	Qst.children.append(('producttype_key__name__icontains', t2))
	Qst.children.append(('technology_key__name__icontains', t3))
	Qst.children.append(('scene_key__name__icontains', t4))
	Qst.children.append(('pricerange_key__name__icontains', t5))

	'''搜索商品'''
	qs = Q()
	qs.children.append(('wareApp_key__name__icontains', search))
	A = models.WareAppPrefix.objects.filter(Q(qs))
	B = []
	C = []
	Ds = None
	if not A:
		'''通过商品搜索器搜索商品'''
		qs = Q()
		qs.connector = 'OR'
		qs.children.append(('classifythere_key__name__icontains', search))
		B = models.WareAppPrefix.objects.filter(Q(qs, ))

		if not B:
			'''通过商品的详细配置参数搜索商品'''
			qs = Q()
			qs.connector = 'OR'
			qs.children.append(('brand__name__icontains', search))
			qs.children.append(('model__icontains', search))
			qs.children.append(('brands__icontains', search))
			qs.children.append(('brands__icontains', search))
			C = models.parameter.objects.filter(qs)
			if C:
				Ds = models.WareAppPrefix.objects.filter(Qst, wareApp_key=C[0].key)

	D = []

	for i in A:
		try:
			ware = i.wareApp_key
			if ware.release == True:
				try:
					image = models.images.objects.filter(key=ware)[:1].get().image
				except:
					image = '/static/images/ware/404.png'
				log.i(globals(), 'A', image)
				D.append({
					'id': ware.id,
					'name': ware.name,
					'money': ware.money,
					'connet': ware.connet,
					'characteristic': ware.characteristic,
					'commodity_description': ware.commodity_description,
					'unix': ware.unix,
					'image': '{}{}'.format(settings.HTTP_HOST, image)
				})
				pass
			log.i(globals(), 'A', i.wareApp_key.name)
		except:
			log.i(globals(), 'A', '通过商品的详细配置参数没有搜索商品')
			pass
		pass
	for i in B:
		try:
			ware = i.wareApp_key
			if ware.release == True:
				try:
					image = models.images.objects.filter(key=ware)[:1].get().image
				except:
					image = '/static/images/ware/404.png'
				log.i(globals(), 'B', image)
				D.append({
					'id': ware.id,
					'name': ware.name,
					'money': ware.money,
					'connet': ware.connet,
					'characteristic': ware.characteristic,
					'commodity_description': ware.commodity_description,
					'unix': ware.unix,
					'image': '{}{}'.format(settings.HTTP_HOST, image)
				})
				pass
			log.i(globals(), 'B', i.wareApp_key.name)
		except:
			log.i(globals(), 'B', '通过商品的详细配置参数没有搜索商品')
			pass
		pass
	for i in C:
		try:
			ware = i.key
			if ware.release == True:
				try:
					image = models.images.objects.filter(key=ware)[:1].get().image
				except:
					image = '/static/images/ware/404.png'

				log.i(globals(), 'C', image)
				D.append({
					'id': ware.id,
					'name': ware.name,
					'money': ware.money,
					'connet': ware.connet,
					'characteristic': ware.characteristic,
					'commodity_description': ware.commodity_description,
					'unix': ware.unix,
					'image': '{}{}'.format(settings.HTTP_HOST, image)
				})
				pass
			log.i(globals(), 'C', i.key.name)
		except:
			log.i(globals(), 'C', '通过商品的详细配置参数没有搜索商品')
			pass

		pass

	log.i(globals(), 'ASD  ', t1, t2, t3, t4, t5)
	ts1, ts2, ts3, ts4, ts5 = None, None, None, None, None
	WarePrefix = None

	''' 获取第一个商品的 搜索筛选器 '''
	filter_error = {}
	if A:
		A1 = A[0]
		WarePrefix = WareSetupPrefix.objects.filter(key=A1.classifythere_key)
		log.i(globals(), 'A1', WarePrefix, A1.classifythere_key.id)
	elif B:
		B1 = B[0]
		WarePrefix = WareSetupPrefix.objects.filter(key=B1.classifythere_key)
		log.i(globals(), 'B1', WarePrefix, B1.wareApp_key.id)
	elif Ds:
		C1 = Ds[0]
		WarePrefix = WareSetupPrefix.objects.filter(key=C1.classifythere_key)
		log.i(globals(), 'C1', WarePrefix, C1.wareApp_key.id)
		pass
	else:
		'''未搜索到商品'''
		WarePrefix = WareSetupPrefix.objects.filter()
		filter_error = {
			'error': '没有搜索到商品'
		}
		pass

	if WarePrefix:
		ts1 = WarePrefix.filter(filter_id='0')[:1].get()
		ts2 = WarePrefix.filter(filter_id='1')[:1].get()
		ts3 = WarePrefix.filter(filter_id='2')[:1].get()
		ts4 = WarePrefix.filter(filter_id='3')[:1].get()
		ts5 = WarePrefix.filter(filter_id='4')[:1].get()

	E = []

	log.i(globals(), 'AAAAAAAAAA ', WarePrefix)
	brand = []
	if ts1: # Q(('name__icontains', t1)) ,
		for i in models.Brand.objects.filter(PrefixKey=ts1):
			brand.append({
				'id': i.id,
				'name': i.name
			})
			pass
		E.append(
			{
				'name': ts1.t1,
				'data': brand
			}
		)
	producttype = []
	if ts2: # Q(('name__icontains', t2)),
		for i in models.ProductType.objects.filter(PrefixKey=ts2):
			producttype.append({
				'id': i.id,
				'name': i.name
			})
			pass
		E.append(
			{
				'name': ts1.t1,
				'data': brand
			}
		)
	technology = []
	if ts3: # Q(('name__icontains', t3)),
		for i in models.Technology.objects.filter(PrefixKey=ts3):
			technology.append({
				'id': i.id,
				'name': i.name
			})
			pass
		E.append(
			{
				'name': ts1.t1,
				'data': brand
			}
		)
	scene = []
	if ts4: # Q(('name__icontains', t4)),
		for i in models.Scene.objects.filter(PrefixKey=ts4):
			scene.append({
				'id': i.id,
				'name': i.name
			})
			pass
		E.append(
			{
				'name': ts1.t1,
				'data': brand
			}
		)
	pricerange = []
	if ts5: # Q(('name__icontains', t5)),
		for i in models.PriceRange.objects.filter(PrefixKey=ts5):
			pricerange.append({
				'id': i.id,
				'name': i.name
			})
			pass
		E.append(
			{
				'name': ts1.t1,
				'data': brand
			}
		)






	try:
		filters = {
			't1': ts1.t1,
			't2': ts2.t2,
			't3': ts3.t3,
			't4': ts4.t4,
			't5': ts5.t5
		}
	except:
		filters = {
		}


	content = {
		'search_ok': Newsearch,
		'search': search,
		'wareapp': D,
		'auth_search': '',
		'E': E,
		'brand': brand,
		'productType': producttype,
		'technology': technology,
		'scene': scene,
		'priceRange': pricerange,
		'Classifications': classify,
		'navigation': nav,
		'navigation_two': navtwo,

		'filter': filters,
		'filter_error': filter_error
	}

	# log.i(globals(), content)
	return render(request, 'defaule/app/search.html', content)
