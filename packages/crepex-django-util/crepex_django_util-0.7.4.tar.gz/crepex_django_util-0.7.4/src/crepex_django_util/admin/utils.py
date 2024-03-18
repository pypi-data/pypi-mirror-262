from django.utils.html import format_html


def get_admin_thumbnail(instance, field):
    """
    관리자 페이지 목록에 이미지 필드를 보여주기 위한 util
    ```
    ie.
    def thumbnail(self, obj):
        return get_admin_thumbnail(obj, 'cover')
    ```
    :param instance: model instance
    :param field: 이미지 필드명
    :return:
    """
    image = getattr(instance, field)
    if image:
        url = getattr(image, 'url', '')
    else:
        url = ''

    if url:
        return format_html(
            '<img src="{profile_thumb}?q=70&s=100x100&t=crop" width="100" />'.format(
                profile_thumb=url,
            )
        )

    return format_html('<span></span>')
