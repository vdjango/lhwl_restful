from django.test import TestCase, override_settings
from account import models

# Create your tests here.

class ProductTest(TestCase):

	@override_settings(DEBUG=False)
	def setUp(self):
		super(ProductTest, self).setUp()
		models.User.objects.create_user(username='1748011755', email='1748011755@qq.com', password='123456789')
		pass



	def tearDown(self):
		User = models.User.objects.get(username='1748011755')

		self.assertEqual(User)
		pass


	pass


