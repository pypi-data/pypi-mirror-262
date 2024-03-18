from django.core.validators import RegexValidator


phone_number_validator = RegexValidator(
    '01[0|1|6|7|8|9]{1}[0-9]{6,8}',
)

only_number_validator = RegexValidator(
    r'^([\d\s]+)$',
)

hex_code_validator = RegexValidator(
    r'^#[\w][^_]{2,5}'
)
