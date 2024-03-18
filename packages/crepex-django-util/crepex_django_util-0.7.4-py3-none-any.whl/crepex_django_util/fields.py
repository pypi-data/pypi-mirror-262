from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .exceptions import GeneralAPIException


class ContentTypeRestrictedSerializerFileField(
    serializers.FileField,
):
    """
    serializer FileField 대용으로 사용
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload.
    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 5242880
    100MB 104857600
    250MB - 214958080
    500MB - 429916160
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        self.alias = kwargs.pop('alias', '')
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            file_size = data.size
            content_type = data.content_type
            value = super().to_internal_value(data)
        except ValidationError as e:
            raise GeneralAPIException(e.detail)

        if self.max_upload_size is not None and file_size > self.max_upload_size:
            max_size = filesizeformat(self.max_upload_size)
            size = filesizeformat(file_size)
            raise GeneralAPIException(f'{self.alias}파일크기는 {max_size} 보다 클 수 없습니다.현재 파일크기는 {size} 입니다.')

        if self.content_types and content_type not in self.content_types:
            raise GeneralAPIException(f'지원되지 않는 {self.alias}파일유형입니다.')

        return value


class ContentTypeRestrictedSerializerImageField(
    ContentTypeRestrictedSerializerFileField,
    serializers.ImageField,
):
    """
    serializer ImageField 대용으로 사용
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload.
    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 5242880
    100MB 104857600
    250MB - 214958080
    500MB - 429916160
    """

    pass


class RepresentProxyRelatedFieldMixin(
    serializers.RelatedField,
):
    """
    외래키 표현과 쓰기를 같은 필드명으로 사용하고 싶을 때 사용
    """

    def __init__(self, **kwargs):
        self.represent_serializer = kwargs.pop('represent_serializer')
        self.represent_kwargs = kwargs.pop('represent_kwargs', {})
        super().__init__(**kwargs)


class RepresentProxyPrimaryKeyRelatedField(
    RepresentProxyRelatedFieldMixin,
    serializers.PrimaryKeyRelatedField,
):

    def to_representation(self, value):
        if self.represent_serializer:
            return self.represent_serializer(
                instance=self.to_internal_value(value.pk),
                context=self.context,
                **self.represent_kwargs,
            ).data
        return super().to_representation(value)


class RepresentProxySlugRelatedField(
    RepresentProxyRelatedFieldMixin,
    serializers.SlugRelatedField,
):

    def to_representation(self, value):
        if self.represent_serializer:
            return self.represent_serializer(
                instance=self.to_internal_value(getattr(value, self.slug_field)),
                context=self.context,
                **self.represent_kwargs,
            ).data
        return super().to_representation(value)


class RelatedRepresentProxyListField(
    serializers.ListField,
):
    """
    Related Field로 기록되는 data를
    ListField로 받아 Validation 하고, 응답은 serializer로 하기 위한 Field
    - 파일필드에 주로 사용
    i.e.
    images = RepresentProxyListField(
        represent_serializer=FileRepresentSerializer,
        required=False,
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False,
        ),
    )
    :param represent_serializer: 응답에 사용할 serializer (required)
    :param queryset_filter: 응답시 가져올 related field filter condition
    """

    def __init__(self, **kwargs):
        self.represent_serializer = kwargs.pop('represent_serializer', None)
        self.queryset_filter = kwargs.pop('queryset_filter', {})
        assert self.represent_serializer, 'Attribute "represent_serializer" is missing'
        super().__init__(**kwargs)

    def to_representation(self, value):
        if self.represent_serializer:
            return self.represent_serializer(
                instance=value,
                many=True,
                context=self.context,
            ).data
        return super().to_representation(value)

    def get_attribute(self, instance):
        manager = getattr(instance, self.field_name)
        return manager.filter(**self.queryset_filter)


class MultipleValuesField(forms.Field):
    """
    다중값 입력 필드
    """
    widget = forms.MultipleHiddenInput
    default_error_messages = {
        'invalid': _('올바른 값을 전달해주세요'),
    }

    def __init__(self, coerce=None, *args, **kwargs):
        self.coerce = coerce
        super().__init__(*args, **kwargs)

    def validate(self, value):
        if self.coerce and isinstance(value, list):
            try:
                value = [self.coerce(v) for v in value]
            except ValueError:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value
