from typing import Dict
from typing import Optional

from django.conf import settings


class ModuleSettings:

    def __init__(self, settings_name: str, defaults: Dict, custom_settings: Optional[Dict] = None):
        self.settings_name = settings_name
        self.defaults = defaults
        if custom_settings:
            self._custom_settings = custom_settings

    @property
    def custom_settings(self):
        if not hasattr(self, '_custom_settings'):
            self._custom_settings = getattr(settings, self.settings_name, {})
        return self._custom_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid setting "%s"' % attr)

        try:
            return self.custom_settings[attr]
        except KeyError:
            return self.defaults[attr]

    def reload(self):
        if hasattr(self, '_custom_settings'):
            delattr(self, '_custom_settings')


def reload_settings_wrapper(module_settings: ModuleSettings):
    """
    반환 callback을 setting_changed signal 에 연결해서 사용
    """
    def reload_settings(*args, **kwargs):
        setting = kwargs['setting']
        if setting == module_settings.settings_name:
            module_settings.reload()
    return reload_settings
