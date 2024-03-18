from django_filters import MultipleChoiceFilter

from .fields import MultipleValuesField


class MultipleValuesFilter(MultipleChoiceFilter):
    """
    여러값을 MultipleChoiceFilter 처럼 사용할 수 있음.
    Choice를 지정하지 않아도 됨.
    :kwargs coerce: 값을 지정한 클래스 타입으로 변경
    """
    field_class = MultipleValuesField
