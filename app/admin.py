from django.contrib import admin

# Register your models here.
from app import models



class SubsectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'time_now']

    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["name"]

    class Meta:
        model = models.Navigation_Two

class ClassificationnAdmin(admin.ModelAdmin):
    list_display = ['name', 'time_now']

    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["name"]

    class Meta:
        model = models.Classification

class Classification_connet_connetnAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'key',  'time_now']

    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["name"]

    class Meta:
        model = models.Classification_There

class Classification_connetAdmin(admin.ModelAdmin):
    list_display = ['subtitle', 'key', 'time_now']

    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["subtitle"]

    class Meta:
        model = models.Classification_Two

class CarouselAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'time_now']

    # 自定义后台过滤器
    list_filter = ["time_add"]


    class Meta:
        model = models.Carousel

class BannerAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["title"]

    class Meta:
        model = models.BannerAd

class Classification_barAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'url', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["name"]

    class Meta:
        model = models.Classification_bar

class HeadlinesAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["title", 'connet']

    class Meta:
        model = models.Headlines

class RecommendAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'user', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["title"]

    class Meta:
        model = models.Recommend


class MiddleTopAdmin(admin.ModelAdmin):
    list_display = ['name', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["name"]

    class Meta:
        model = models.MiddleTop


class commodityAdmin(admin.ModelAdmin):
    list_display = ['title', 'money', 'time_now']
    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["title"]

    class Meta:
        model = models.commodity


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    # 自定义后台过滤器

    # 自定义后台搜索
    search_fields = ['name']

    class Meta:
        model = models.Choice




class ChoiceoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    # 自定义后台过滤器

    # 自定义后台搜索
    search_fields = ['name']

    class Meta:
        model = models.Lease


class ChoicetwoAdmin(admin.ModelAdmin):
    list_display = ['name']
    # 自定义后台过滤器

    # 自定义后台搜索
    search_fields = ['name']

    class Meta:
        model = models.Duration




admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.commodity, commodityAdmin)
admin.site.register(models.MiddleTop, MiddleTopAdmin)
admin.site.register(models.Recommend, RecommendAdmin)
admin.site.register(models.Headlines, HeadlinesAdmin)
admin.site.register(models.Carousel, CarouselAdmin)
admin.site.register(models.Classification_bar, Classification_barAdmin)
admin.site.register(models.Classification_Two, Classification_connetAdmin)
admin.site.register(models.Classification_There, Classification_connet_connetnAdmin)
admin.site.register(models.Classification, ClassificationnAdmin)
admin.site.register(models.Navigation_Two, SubsectionAdmin)
admin.site.register(models.BannerAd, BannerAdAdmin)

