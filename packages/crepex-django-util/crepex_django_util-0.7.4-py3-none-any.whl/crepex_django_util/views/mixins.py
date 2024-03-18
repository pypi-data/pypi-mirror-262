from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.generics import GenericAPIView

from .generics import BaseCreateAPIView


class ExtraUrlDataMixin(
    GenericAPIView,
):
    """
    View 에 추가 데이터를 전달하기 위한 Mixin
    """

    @classmethod
    def as_view(cls, extra=None, **kwargs):
        assert extra, 'View requires extra kwargs'
        cls.extra = extra
        return super().as_view(**kwargs)


class ExtraDataToContextMixin(
    ExtraUrlDataMixin,
):
    """
    Serializer 에 as_view 에 정의한 데이터를 Context 로 전달.
    """
    extra_ctx_field = "extra"

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({self.extra_ctx_field: self.extra})
        return ctx


class CurrentUserAssetMixin(
    ExtraUrlDataMixin,
    GenericAPIView,
):
    """
    현재 인증된 유저로 queryset 필터
    - `as_view(extra={'me': True})` 로 사용
    """

    user_field = 'user_id'

    def get_queryset(self):
        assert self.extra.get('me'), 'Extra value is not True'
        queryset = super().get_queryset()

        user = self.request.user
        if user.is_authenticated:
            filter_kwargs = {self.user_field: user.id}
            queryset = queryset.filter(**filter_kwargs)
        return queryset

    def get_object(self):
        assert self.extra.get('me'), 'Extra value is not True'

        if self.request.user.is_authenticated:
            queryset = self.filter_queryset(self.get_queryset())
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            if self.kwargs.get(lookup_url_kwarg):
                filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            else:
                filter_kwargs = {}

            obj = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, obj)
            return obj
        else:
            raise PermissionDenied()


class ListSerializerMixin(
    GenericAPIView,
):
    """
    Serializer 에 many=True 를 동적으로 전달하기 위한 method
    보통 Multiple create or update 에 사용.

    get_serializer override 시 api doc 제대로 나오지 않는 문제에 따라
    super()... 호출이 아닌 직접 호출로 구현
    https://github.com/tfranzel/drf-spectacular/issues/386
    """

    list_allow_methods = ['POST']

    def get_serializer(self, *args, **kwargs):
        serializer_class = super().get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.request.method in self.list_allow_methods:
            kwargs.update({'many': True})
        return serializer_class(*args, **kwargs) if serializer_class else Serializer()


class PublishedObjectOnlyMixin(GenericAPIView):
    """
    공개된 queryset 필터
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(queryset.model, 'is_published'):
            return queryset.filter(is_published=True)
        return queryset


class WriterCanReadAllContentMixin(
    GenericAPIView,
):
    """
    특정 필드에 의해 필터되는 queryset이 있을때, 유저 필드가 있다면
    로그인한 유저는 필터와 관계없이 유저로 필터된 데이터를 확인할 수 있다.
    """

    condition_field = 'is_published'

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(queryset.model, self.condition_field):
            filtered = queryset.filter(**{self.condition_field: True})
            user = self.request.user
            if hasattr(queryset.model, 'user') and user.is_authenticated:
                return filtered | queryset.filter(user=user, **{self.condition_field: False})
            else:
                return filtered
        return queryset


class FieldsLookupFromUrlMixin(
    GenericAPIView,
):
    """
    URL Path 에서 주어진 Field 명의 값들을 모두 찾아 Queryset 필터에 추가한다.
    :param lookup_url_fields: 탐색에 필요한 옵션 지정
    - lookup_field: 탐색하고자 하는 Field
    - lookup_url_kwarg: URL에 명시된 Field key, 미지정시 lookup_field 사용
    - lookup_expr: 탐색시 사용되는 표현식 , 미지정시 exact(일치) 사용
    """
    lookup_url_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        qs_kwargs = {}
        for field in self.lookup_url_fields:
            lookup_field = field['lookup_field']
            lookup_url_kwarg = field.get('lookup_url_kwarg', lookup_field)
            lookup_expr = field.get('lookup_expr', 'exact')
            url_value = self.kwargs[lookup_url_kwarg]
            if url_value:
                qs_kwargs.update({f'{lookup_field}__{lookup_expr}': url_value})

        queryset = queryset.filter(**qs_kwargs)

        return queryset


class FieldsCreateFromUrlMixin(
    BaseCreateAPIView,
):
    """
    URL Path 에서 주어진 Field 명의 값들을 모두 찾아 CreateAPI serializer field 에 추가한다
    :param lookup_url_fields: 탐색에 필요한 옵션 지정
    - lookup_field: 탐색하고자 하는 Field
    - lookup_url_kwarg: URL에 명시된 Field key, 미지정시 lookup_field 사용
    - lookup_model: 값이 아닌 객체 전달시 탐색할 model
    - lookup_expr: 객체 탐색시 사용되는 표현식 , 미지정시 exact(일치) 사용
    """

    lookup_url_fields = []

    def perform_create(self, serializer, **kwargs):
        extra_data_kwargs = {}
        for field in self.lookup_url_fields:
            lookup_field = field['lookup_field']
            lookup_url_kwarg = field.get('lookup_url_kwarg', lookup_field)
            lookup_expr = field.get('lookup_expr', '')
            model = field.get('lookup_model')
            value = self.kwargs.get(lookup_url_kwarg)

            if model:
                try:
                    value = model.objects.get(**{lookup_expr: value})
                except model.DoesNotExist:
                    raise ValidationError({lookup_field: '찾을 수 없습니다'})

            extra_data_kwargs.update({lookup_field: value})
        super().perform_create(serializer, **kwargs, **extra_data_kwargs)
