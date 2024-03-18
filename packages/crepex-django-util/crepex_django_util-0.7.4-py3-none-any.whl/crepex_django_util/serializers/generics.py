from rest_framework import serializers


class IntListSerializer(serializers.ListSerializer):

    child = serializers.IntegerField()


class CharListSerializer(serializers.ListSerializer):

    child = serializers.CharField()


class CodeSerializer(serializers.Serializer):

    code = serializers.CharField()


class FileRepresentWithIDSerializer(
    serializers.HyperlinkedModelSerializer,
):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'path': self.context['request'].build_absolute_uri(instance.path),
        }


class FileRepresentSerializer(
    serializers.Serializer,
):

    def to_representation(self, instance):
        return self.context['request'].build_absolute_uri(instance.path)
