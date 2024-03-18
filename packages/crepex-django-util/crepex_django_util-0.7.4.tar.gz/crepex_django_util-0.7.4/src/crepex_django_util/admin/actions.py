import csv
from typing import Optional
from typing import Dict

from django.http import HttpResponse


def export_as_csv_action(
    description="선택된 정보 CSV 파일로 출력",
    fields=None,
    exclude=None,
    header=True,
    force_fields=True,
    charset='utf-8-sig',
):
    """
    CSV 출력을 하는 Django Admin Action Function \n
    :param description: Action 에 표시할 문구
    :param fields: 출력 할 Model Field(Column)
    :param exclude: 출력에서 제외할 Model Field
    :param header: Field(Column) 이름을 첫번째 행으로 출력할지 여부
    :param force_fields: Django admin 의 list_display 의 Custom field (문자열) 을 사용할 지 여부 False 인 경우 Model 에 없는 필드는 제외한다.
    :param charset: encoding type
    """
    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        if not force_fields:
            field_names = set([field.name for field in opts.fields])
            if fields:
                field_set = set(fields)
                field_names = field_names & field_set
        elif fields:
            field_names = set(fields)
        else:
            raise ValueError('올바른 옵션을 넣어주세요.')
        if exclude:
            exclude_set = set(exclude)
            field_names = field_names - exclude_set

        response = HttpResponse(content_type='text/csv', charset=charset)
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)

        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            row = []
            for field in field_names:
                try:
                    if callable(getattr(obj, field)):
                        row.append(str(getattr(obj, field)()))
                    else:
                        row.append(str(getattr(obj, field)))
                except AttributeError:
                    row.append(str((getattr(modeladmin, field)(obj))))
                except Exception:
                    raise
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    export_as_csv.__name__ = description
    return export_as_csv


def update_queryset_action(
    fields: Dict,
    condition: Optional[Dict],
    model_label='정보',
    state_label='공개상태로',
):
    """
    선택된 row에 대해 지정된 fields를 적용하여 Update
    :param fields: 업데이트 할 필드명, 값의 Dict
    :param condition: queryset 추가 필터조건
    :param model_label: 모델 라벨
    :param state_label: 상태 업데이트 라벨
    :return:
    """
    def wrapped_update_queryset_action(modeladmin, request, queryset):
        if condition:
            queryset = queryset.filter(**condition)
        queryset.update(**fields)
    wrapped_update_queryset_action.short_description = f'선택된 {model_label} 모두 {state_label} 바꾸기'
    wrapped_update_queryset_action.__name__ = f'{model_label}_{state_label}'
    return wrapped_update_queryset_action
