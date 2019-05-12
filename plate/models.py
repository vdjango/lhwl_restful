from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from slugify import slugify


class plateModels(models.Model):
    '''
    导航页面 [涵盖导航 二级导航]

    类似于 文章等
    '''
    name = models.CharField(max_length=200, verbose_name='板块名称')
    slug = models.SlugField(max_length=200, verbose_name='slugify(name)')

    time_add = models.DateTimeField(auto_now_add=True)
    time_now = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.time_add:
            self.time_add = timezone.now()

        super(plateModels, self).save(*args, **kwargs)
        pass

    def get_absolute_url(self):
        return reverse('plate:index', args=[self.id, self.slug])



    def __str__(self):
        return self.name
    pass


class plateContent(models.Model):
    '''页面板块'''
    name = models.CharField(max_length=200, verbose_name='板块标题')
    content = models.ForeignKey('app.Classification_There', on_delete=models.SET_NULL, null=True, verbose_name='')
    number = models.IntegerField(default=10, verbose_name='商品查询数量')
    key = models.ForeignKey(plateModels, on_delete=models.CASCADE, null=True)

    time_add = models.DateTimeField(auto_now_add=True)
    time_now = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.time_add:
            self.time_add = timezone.now()

        super(plateContent, self).save(*args, **kwargs)
        pass

    def get_wareappprefix_set(self):
        return self.content.wareappprefix_set.filter()[:10]

