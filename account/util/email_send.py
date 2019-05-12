from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from account import models  # 邮箱验证model
from lhwill.util import log
from managestage.utli.datetimenow import datetimenow
from account.util.AtomSign import AtomSig
from lhwill import settings


# 生成随机字符串
def random_str(randomlength=8):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def authUrl(request, code, email, stype='register'):
	if stype == 'register':
		url = "{}/auth/active/{}/?email={}".format(settings.HTTP_HOST, code, email)
	else:
		url = "{}/auth/auth_retrieve/?email={}&auto={}".format(settings.HTTP_HOST, email, code)

	url, salt = AtomSig(request, url, stype='lock')
	print('重置验证码，生成Sign数据库验证', salt, email)
	salts = bytes.decode(salt)

	M = models.Md5Salt.objects.filter(email=email)
	print('重置验证码，生成Sign数据库验证', M)
	if M:

		for i in M:
			i.salt = salts
			i.save()
		pass
	else:
		models.Md5Salt(
			email=email,
			salt=salts,
			key=models.User.objects.get(email=email),
			time_add=datetimenow(),
			time_now=datetimenow()
		).save()
	return url


def send_auth_email(request, send_type="register", Users=None):
	'''

	:param request:
	:param email:
	:param send_type: register[注册账号]/retrieve[找回密码]
	:return:
	'''

	if Users == None:
		username = request.user.username
	else:
		username = Users[0].username

	user = models.User.objects.filter(username=username)
	code = random_str(128)
	print(user[0].username)
	if user:
		username = user[0]
		email_record = models.UserProfix.objects.filter(email=username.email)
		if email_record:
			for i in email_record:
				i.code = code
				i.email = username.email
				i.oneKey = username
				i.send_type = send_type
				i.addtime = datetimenow()
				if send_type == "register":
					i.defaule = False
				if send_type == 'retrieve':
					i.code_default = True
				i.save()
			pass
		else:
			email_record = models.UserProfix()
			email_record.username = username.username
			email_record.email = username.email
			email_record.oneKey = username
			email_record.code = code
			email_record.send_type = send_type
			email_record.addtime = datetimenow()
			if send_type == "register":
				email_record.defaule = False
			if send_type == 'retrieve':
				email_record.code_default = True
			email_record.save()

		email_record = models.UserProfix.objects.filter(username=username.username)

		email_title, email_body = None, None

		# 如果为注册类型
		if send_type == "register":
			url = authUrl(request, code, email_record[0].email, stype='register')
			email_title = "注册激活链接"
			email_body = "请点击下面的链接激活你的账号: {}".format(url)
			print(email_title)
		if send_type == 'retrieve':
			url = authUrl(request, code, email_record[0].email, stype='retrieve')
			email_title = '找回密码验证'
			email_body = "请点击下面的链接跳转到您将要找回密码的地址: {}".format(url)

		print(email_title)
		mail(username.email, email_title, email_body)


from lhwill import settings
from managestage.models import systemmail


class Email(object):

	def __init__(self):
		self.systeme = systemmail.objects.filter()
		self.host = self.get_Emailhost()
		self.port = self.get_Emailport()
		self.user = self.get_Emailuser()
		self.password = self.get_Emailpassword()
		pass

	def get_Emailhost(self):
		'''
		设置邮箱地址
		:return:
		'''
		systeme = self.systeme
		if systeme:
			settings.EMAIL_HOST = systeme[0].host
			print('EMAIL_HOST', settings.EMAIL_HOST)
		return settings.EMAIL_HOST
		pass

	def get_Emailport(self):
		'''
		设置邮箱端口
		:return:
		'''
		systeme = self.systeme
		if systeme:
			settings.EMAIL_PORT = systeme[0].port
			print('EMAIL_PORT', settings.EMAIL_PORT)
		return settings.EMAIL_PORT
		pass

	def get_Emailuser(self):
		'''
		设置邮箱用户
		:return:
		'''
		systeme = self.systeme
		if systeme:
			settings.EMAIL_HOST_USER = systeme[0].user
			print('EMAIL_HOST_USER', settings.EMAIL_HOST_USER)
		return settings.EMAIL_HOST_USER
		pass

	def get_Emailpassword(self):
		'''
		设置邮箱密码
		:return:
		'''
		systeme = self.systeme
		if systeme:
			settings.EMAIL_HOST_PASSWORD = systeme[0].passwd
			print('EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD)
		return settings.EMAIL_HOST_PASSWORD
		pass

	def set_host(self, host):
		self.host = host
		pass

	def set_port(self, port):
		self.port = port
		pass

	def set_user(self, user):
		self.user = user
		pass

	def set_password(self, password):
		self.password = password

	def send_mail(self, email_user, email_title=None, email_body=None):
		mail(email_user=email_user, email_title=email_title, email_body=email_body)
	pass


def mail(email_user, email_title=None, email_body=None):
	'''
	发送邮件
	:param email_user:
	:param code:
	:param args:
	:return:
	'''

	send_status = False
	try:
		if email_user:

			send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email_user])
			if send_status:
				log.i(globals(), '发送邮件成功')
				pass
	except Exception as e:
		log.i(globals(), '发送邮件失败，抛出异常', e.args)
		pass

	return send_status
