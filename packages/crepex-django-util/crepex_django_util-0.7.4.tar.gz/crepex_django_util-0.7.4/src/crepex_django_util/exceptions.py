from rest_framework import exceptions
from rest_framework import status


class GeneralAPIException(exceptions.APIException):

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        if isinstance(detail, (str, list)):
            error_dict = {
                'error': {
                    'message': detail,
                }
            }
            if code:
                error_dict['error']['code'] = code
            self.detail = error_dict
        else:
            super().__init__(detail, code)
