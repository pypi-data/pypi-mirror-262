from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ..exceptions import GeneralAPIException


class DynamicReadonlyFieldsMixin(
    serializers.Serializer,
):
    """
    특정 필드를 Serializer 읽기전용으로 사용할 때 사용
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('dynamic_read_only_fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            readonly_fields = set(fields)
            for field_name in readonly_fields:
                self.fields[field_name].read_only = True


class DynamicExcludeFieldsMixin(
    serializers.Serializer,
):
    """
    특정 필드를 Serializer 에서 사용하지 않을 때 사용
    """

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)

        super().__init__(*args, **kwargs)

        if exclude is not None:
            exclude_fields = set(exclude)
            existing = set(self.fields.keys())
            for field_name in existing & exclude_fields:
                self.fields.pop(field_name)


class UniqueUserValidateMixin(
    serializers.Serializer,
):
    """
    고유 유저키 검사
    """

    def validate(self, attrs):
        options = getattr(self.Meta, 'unique_user_validator', {})
        error_message = options.get('error_message', '이미 생성되었습니다')
        user = self.context['request'].user
        attrs = super().validate(attrs)

        # 업데이트 요청은 Pass
        if self.instance:
            return attrs

        if user.is_authenticated and self.Meta.model.objects.filter(user=user).exists():
            raise GeneralAPIException(error_message)
        return attrs


class BulkChildrenCreateUpdateMixin:
    """
    related serializer 의 다중 생성/수정을 위한 mixin
    하위 serializer 에는 primary_field 와 일치하는 필드(ex: id)가
    relatedField 형식으로 선언되어 있어야 한다.

    id = serializers.PrimaryKeyRelatedField(
        queryset=ChildrenModel.objects.all(),
        required=False,  # Update 시 id 누락 객체 처리
    )
    """

    def process_bulk_update(
        self,
        data_list,
        model,
        update_fields,
        primary_key='id',
    ):
        instances = {}
        for data in data_list:
            if primary_key not in data:
                continue
            obj = data[primary_key]
            update_instance = instances.setdefault(obj, obj)
            for k, v in data.items():
                if k != primary_key:
                    setattr(update_instance, k, v)
        will_update = instances.values()
        if will_update:
            model.objects.bulk_update(will_update, update_fields)

    def pre_bulk_create(self, parent_field: str, will_create: list):
        return will_create

    def process_bulk_create(self, model, parent, parent_field: str, create_data: list,):
        will_create = [
            model(**data, **{parent_field: parent}) for data in create_data
        ]
        if will_create:
            return model.objects.bulk_create(self.pre_bulk_create(parent_field, will_create))
        return []

    def bulk_create(self, parent, create_data: list, key=None):
        results = {}
        for model_data in self.Meta.children_models:
            # 모델이 여러개인 경우 식별을 위함
            if model_data.get('key') and model_data['key'] != key:
                continue
            model = model_data['model']
            parent_field = model_data['parent_field']
            result = self.process_bulk_create(model, parent, parent_field, create_data)
            results[model_data.get('key')] = result
        return results

    def bulk_update(self, update_data: list, key=None):
        for model_data in self.Meta.children_models:
            if model_data.get('key') and model_data['key'] != key:
                continue
            model = model_data['model']
            fields = model_data['update_fields']
            primary_field = model_data.get('primary_field', 'id')
            self.process_bulk_update(update_data, model, fields, primary_field)

    def update_or_create(self, parent, update_data: list, key=None):
        create_results = {}
        for model_data in self.Meta.children_models:
            model_key = model_data.get('key')

            if model_key and model_key != key:
                continue

            model = model_data['model']
            parent_field = model_data['parent_field']
            primary_field = model_data.get('primary_field', 'id')

            create_data = []
            update_objs = {}

            for data in update_data:
                if primary_field in data:
                    update_objs[data[primary_field]] = data
                else:
                    create_data.append(data)

            created_objs = self.process_bulk_create(model, parent, parent_field, create_data)
            create_results[model_key] = created_objs
            self.bulk_update(list(update_objs.values()), key=key)

            if model_data.get('exist_or_delete', True):
                child_field = model_data['child_field']
                created_ids = list(map(lambda o: getattr(o, primary_field), created_objs))
                # 방금 생성된 객체와 업데이트 대상이었던 객체는 삭제 X
                all_children = getattr(parent, child_field).exclude(
                    **{f'{primary_field}__in': created_ids},
                )

                for existed in all_children:
                    if existed not in update_objs:
                        existed.delete()
        return create_results


class DynamicSerializerMethodFieldMixin(
    serializers.Serializer,
):
    """
    동적 serializer method field 생성기
    i.e.
    class Meta:
        dynamic_method_fields = [
        {
            'name': 'images',
            'serializer': FileRepresentSerializer,
            'instance_getter': lambda obj: obj.images.all(),
            'field_schema': serializers.ListSerializer(child=serializers.ImageField()),
            'field_kwargs': {
                'label': '이미지',
            }
        }
    ]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert hasattr(self, 'Meta'), (
            'Class {serializer_class} missing "Meta" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        assert hasattr(self.Meta, 'dynamic_method_fields'), (
            'Attribute "dynamic_method_fields" is missing class Meta'
        )

        for option in self.Meta.dynamic_method_fields:
            name = option['name']
            serializer = option['serializer']
            instance_getter = option['instance_getter']
            field_schema = option['field_schema']
            field_kwargs = option.get('field_kwargs', {})

            setattr(self, f'get_{name}', self._get_field_method(serializer, instance_getter, field_schema))
            self.fields[name] = serializers.SerializerMethodField(
                **field_kwargs,
            )

    def _get_field_method(self, serializer, instance_getter, field_schema):
        @extend_schema_field(field_schema)
        def serializer_method_field(obj):
            return serializer(
                context=self.context,
                instance=instance_getter(obj),
                many=True,
            ).data
        return serializer_method_field
