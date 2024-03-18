from django.apps import apps


def get_model(str_model: str):
    """
    동적으로 모델을 import 할 때 사용
    """
    return apps.get_model(*str_model.split('.', 1))
