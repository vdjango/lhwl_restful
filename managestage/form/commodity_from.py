from django import forms
from django.utils.datastructures import MultiValueDictKeyError

from app import models
from lhwill.util.log import log

logger = log(globals())


class FilterModelsForm(forms.ModelForm):
    '''
    Filter Form validating form
    You need to include the name attribute.
    '''

    # Verification name
    verify = None
    verify_info = {}

    def add_prefix(self, field_name):
        """
        Return the field name with a prefix appended, if this Form has a
        prefix set.

        Subclasses may wish to override.
        """
        if not self.verify:
            return None

        return '%s' % self.verify[0]

    def clean_name(self):
        if not self.verify:
            self.verify = ['name']
            return self.cleaned_data['name']

        try:
            data = self.data[self.verify[0]]
        except MultiValueDictKeyError as e:
            raise forms.ValidationError('此字段不能为空。')

        return data

    pass


class WareAppModelForm(forms.ModelForm):
    '''
    商品提交表单验证
    '''
    verify = ['name']
    verify_info = {
        'name': '商品名称未填写'
    }

    class Meta:
        model = models.WareApp
        fields = ['name', 'connet', 'unix']



class BrandModelForm(FilterModelsForm):
    verify = ['t0']
    verify_info = {
        't0': '筛选器字段未填写'
    }

    class Meta:
        model = models.Brand
        fields = ['name']


class SceneModelForm(FilterModelsForm):
    verify = ['t3']
    verify_info = {
        't3': '筛选器字段未填写'
    }

    class Meta:
        model = models.Scene
        fields = ['name']


class TechnologyModelForm(FilterModelsForm):
    verify = ['t2']
    verify_info = {
        't2': '筛选器字段未填写'
    }

    class Meta:
        model = models.Technology
        fields = ['name']


class PriceRangeModelForm(FilterModelsForm):
    verify = ['t4']
    verify_info = {
        't4': '筛选器字段未填写'
    }

    class Meta:
        model = models.PriceRange
        fields = ['name']


class ProductTypeModelForm(FilterModelsForm):
    verify = ['t1']
    verify_info = {
        't1': '筛选器字段未填写'
    }

    class Meta:
        model = models.ProductType
        fields = ['name']


class ClassificationModelForm(FilterModelsForm):
    verify = ['classify_id']
    verify_info = {
        'classify_id': '一级分类字段未填写'
    }

    class Meta:
        model = models.Classification
        fields = ['name']


class Classification_ThereModelForm(FilterModelsForm):
    verify = ['classifytwo_id']
    verify_info = {
        'classifytwo_id': '子分类字段未填写'
    }

    class Meta:
        model = models.Classification_There
        fields = ['name']


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = models.images
        fields = ['image']


class ParameterModelForm(FilterModelsForm):
    class Meta:
        model = models.parameter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParameterModelForm, self).__init__(*args, **kwargs)
        self.fields['key'].required = False
        self.fields['brands'].required = False
        self.fields['model'].required = False
        self.fields['productType'].required = False
        self.fields['colorType'].required = False
        self.fields['coverFunction'].required = False
        self.fields['velocityType'].required = False
        self.fields['maximumOriginalSize'].required = False
        self.fields['memory'].required = False
        self.fields['hardDisk'].required = False
        self.fields['forPaperCapacity'].required = False
        self.fields['mediumWeight'].required = False
        self.fields['materialDescription'].required = False
        self.fields['doubleSidedDevice'].required = False
        self.fields['automaticDrafts'].required = False
        self.fields['networkFunction'].required = False
        self.fields['highestCv'].required = False
        self.fields['falsrom'].required = False
        self.fields['other'].required = False
        self.fields['photocopyingSpeed'].required = False
        self.fields['PhotocopyingResolution'].required = False
        self.fields['copySize'].required = False
        self.fields['preheatingTime'].required = False
        self.fields['copyPhotocopyingPage'].required = False
        self.fields['continuityXeroxPages'].required = False

        self.fields['zoomRange'].required = False
        self.fields['copyOdds'].required = False
        self.fields['printController'].required = False
        self.fields['printingSpeed'].required = False
        self.fields['printResolution'].required = False
        self.fields['printLanguage'].required = False
        self.fields['printingOtherPerformance'].required = False
        self.fields['scanningController'].required = False
        self.fields['scanningResolution'].required = False
        self.fields['outputFormat'].required = False
        self.fields['scanningOtherPerformance'].required = False
        self.fields['facsimileController'].required = False
        self.fields['modemSpeed'].required = False
        self.fields['dataCompressionMethod'].required = False
        self.fields['faxOtherPerformance'].required = False
        self.fields['display'].required = False
        self.fields['mainframeSize'].required = False
        self.fields['weight'].required = False
        self.fields['otherFeatures'].required = False
        self.fields['timeMarket'].required = False
        self.fields['optionalAccessories'].required = False
        self.fields['warrantyTime'].required = False
        self.fields['customerService'].required = False
        self.fields['detailedContent'].required = False
        self.fields['brand'].required = False
        self.fields['time_add'].required = False

        for v in self.data:
            data = self.data[v]
            if not data:
                try:
                    self.fields[v].required = True
                except KeyError:
                    pass


