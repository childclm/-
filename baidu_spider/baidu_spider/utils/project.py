from baidu_spider.baidu_spider.settings.settings_manage import SettingsManger
import os
import sys
from importlib import import_module


def get_settings(modul):
    _settings = SettingsManger({'project': 'sjdfo'})
    _settings.set_settings(modul)
    _init_env()
    return _settings


def _get_closest(path='.'):
    path = os.path.abspath(path)
    return path


def _init_env():
    closest = _get_closest()
    if closest:
        project_dir = os.path.dirname(closest)
        sys.path.append(project_dir)


def merge_settings(spider, settings):
    if hasattr(spider, 'custom_settings'):
        custom_settings = getattr(spider, 'custom_settings')
        settings.update(custom_settings)


def load_class(_path):
    if not isinstance(_path, str):
        if callable(_path):
            return _path
        else:
            raise TypeError(f'args expected string or object, get {type(_path)}')
    model, name = _path.rsplit('.', 1)
    mod = import_module(model)
    try:
        cls = getattr(mod, name)
    except AttributeError:
        raise NameError(f"mode {model!r} has no attribute {name}")
    return cls


