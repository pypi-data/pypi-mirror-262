from collections import OrderedDict

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from ..serializers.generics import IntListSerializer


class BaseCreateAPIView(
    generics.CreateAPIView,
):

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)


class CurrentUserCreateAPIView(
    BaseCreateAPIView,
):

    user_field = 'user_id'

    def perform_create(self, serializer, **kwargs):
        if self.user_field and self.request.user.is_authenticated:
            kwargs.update({self.user_field: self.request.user.id})
        super().perform_create(serializer, **kwargs)


class BaseListAPIView(
    generics.ListAPIView,
):
    pass


class RawDataListAPIView(
    BaseListAPIView,
):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", len(data)),
                    ("next", None),
                    ("previous", None),
                    ("results", data),
                ]
            )
        )


class BaseRetrieveAPIView(
    generics.RetrieveAPIView,
):
    pass


class BaseUpdateAPIView(
    generics.UpdateAPIView,
):

    lookup_field = 'id'


class BaseDestroyAPIView(
    generics.DestroyAPIView,
):

    lookup_url_kwarg = 'id'

    def get_destroy_response(self):
        if self.lookup_url_kwarg:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    self.lookup_url_kwarg: self.kwargs.get(self.lookup_url_kwarg, None),
                },
            )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = self.get_destroy_response()
        return response


class MultipleDestroyAPIView(
    BaseDestroyAPIView,
):

    """
    다중삭제를 위한 Generic View
    - 기본동작은 ID 목록(Int)을 받아 필터링해 삭제
    """

    destroy_serializer_class = IntListSerializer
    lookup_expr = '__in'

    def get_serializer_class(self):
        if self.request.method == 'DELETE':
            return self.destroy_serializer_class
        return super().get_serializer_class()

    def get_lookup_data(self, serializer):
        return serializer.validated_data

    def get_queryset_for_destroy(self, serializer):
        lookup_data = self.get_lookup_data(serializer)
        lookup_field = f'{self.lookup_field}{self.lookup_expr}'

        qs = self.filter_queryset(self.get_queryset())
        qs = qs.filter(**{lookup_field: lookup_data})
        return qs

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset_for_destroy(serializer)
        self.perform_destroy(qs)

        response = self.get_destroy_response()
        return response

    def perform_destroy(self, qs):
        qs.delete()
