from copy import deepcopy
from importlib import import_module  # 动态导入包
from baidu_spider.baidu_spider.settings import default_settings
from collections.abc import MutableMapping


class SettingsManger(MutableMapping):
    def __init__(self, values=None):
        self.attributes = {}
        self.set_settings(default_settings)
        self.update_values(values)

    def __getitem__(self, key):
        if key not in self:
            return None
        return self.attributes[key]

    def get(self, key, default=None):
        return self[key] if key is not None else default

    def __contains__(self, key):
        return key in self.attributes

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def set(self, key, value):
        self[key] = value

    def __delitem__(self, key):
        del self.attributes[key]

    def delete(self, key):
        del self.attributes[key]

    def __len__(self):
        return len(self.attributes)

    def __iter__(self):
        return iter(self.attributes)

    def set_settings(self, module):
        if isinstance(module, str):
            # 如果是字符串，我们则实现动态导入
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getbool(self, name, default=False) -> bool:
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ('True', 'true', 'TRUE'):
                return True
            if got in ('False', 'false', 'FALSE'):
                return False
            raise ValueError('Supported values are: (0 or 1), ("0" or "1"), (True or False), (true or false), '
                             '(TRUE or FALSE), ("TRUE" or "FALSE"),'' ("True" or "False"), ("true" or "false") ')

    def getlist(self, name, default=None):
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(',')
        return list(value)

    def __str__(self):
        return f'Settings values={self.attributes}'

    __repr__ = __str__

    def update_values(self, values):
        if values is not None:
            for key, value in values.items():
                self[key] = value

    def copy(self):
        return deepcopy(self)


if __name__ == '__main__':
    settings = SettingsManger()
    settings.set('aba', 'sdjf')
    settings.delete('aba')
    print(settings)
    print(settings.items())
