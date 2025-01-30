from ._init import *
from PySide2.QtCore import QSettings as __QSettings
from _typeshed import Incomplete

__all__ = [
    'project',
    'exporters',
    'aux_exporters',
    'aux_importers',
    'mediaio',
    'ui'
]

REGISTRY_COMPANY_NAME: Incomplete
REGISTRY_APPLICATION_NAME: Incomplete
APPLICATION_NAME: Incomplete

class Settings(__QSettings):
    override: Incomplete
    read_overridden: Incomplete
    def __init__(self, override: bool = False, read_overridden: bool = True) -> None: ...
    def setValue(self, key, value) -> None: ...
    def value(self, key, default: Incomplete | None = None): ...
    def childKeys(self): ...
    def childGroups(self): ...
    def allKeys(self): ...
    class SettingAccessor:
        value_types: Incomplete
        def __init__(self, key, default_value: Incomplete | None = None, choices=...) -> None: ...
        def __get__(self, instance, owner): ...
        def __set__(self, instance, value) -> None: ...
    class SettingAccessorCoupler:
        def __init__(self, mapper_data) -> None: ...
        def __get__(self, instance, owner): ...
        def __set__(self, instance, value) -> None: ...
    class CustomSettingAccessor:
        def __init__(self, custom_getter, custom_setter) -> None: ...
        def __get__(self, instance, owner): ...
        def __set__(self, instance, value) -> None: ...
    class StringSettingAccessor(SettingAccessor):
        value_types = str
    class BooleanSettingAccessor(SettingAccessor):
        value_types = bool
        def __get__(self, instance, owner): ...
    class IntegerSettingAccessor(SettingAccessor):
        value_types = int
    class FloatSettingAccessor(SettingAccessor):
        value_types = float
    disable_offscreen_buffers: Incomplete
    enable_cl_tracker: Incomplete
    absolute_output_dir: Incomplete
    absolute_output_dir_enabled: Incomplete
    relative_output_dir: Incomplete
    output_format: Incomplete
    undo_history_size: Incomplete
    gpu_device: Incomplete
    use_with_ae: Incomplete

def get_mocha_exec_name(app=...): ...
def run_mocha(app=..., footage_path: str = '', **kwargs): ...
