from django.shortcuts import render

from app.views import About


class Us(About):
	template_name = 'defaule/about/about.html'

	def get(self, request):
		return render(request, self.template_name)

	pass



