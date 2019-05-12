from django.db import models

# Create your models here.
from lhwill import settings


class api(models.Model):
    url = models.URLField(verbose_name='API root')
    version = models.CharField(max_length=10, verbose_name='Api版本号')

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = settings.HTTP_HOST
            pass
        if not self.version:
            self.version = '0.1.0'

        super(api, self).save(*args, **kwargs)
