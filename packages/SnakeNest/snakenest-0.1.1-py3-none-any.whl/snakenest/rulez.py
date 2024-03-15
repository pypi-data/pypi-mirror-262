from re import findall
from os.path import exists
from yaml import full_load as load_yaml_file
from os import environ


# https://matthewpburruss.com/post/yaml/
# https://pyyaml.org/wiki/PyYAMLDocumentation
class Rulez:
    def __init__(self, file_):
        self.__prop = {}
        self.__rulez = {}
        if exists(file_):
            with open(file_) as f:
                self.__rulez = load_yaml_file(f)

    def __get(self, val, name):
        _max = len(val)
        obj = self.__rulez
        for i in range(_max):
            if val[i] in obj:
                if i == _max - 1:
                    a = obj[val[i]]
                    self.__prop[name] = a
                    return a
                else:
                    obj = obj[val[i]]
        return ''

    def __get_from_env(self):
        pass

    def get(self, item: str, default=None):
        search = item
        default_item = default

        matches = findall('\\${(.*?)}', item)
        has_match = len(matches) > 0

        if has_match > 0:
            split = matches[0].split(':')
            if len(split) > 1:
                default_item = split[1]
            search = split[0]

        if search in self.__prop:
            return self.__prop[search]

        val = search.split('.')
        value = self.__get(val, search)
        if value != '':
            return value

        if has_match and not default_item:
            raise AttributeError(f'rule {matches[0]} no set')

        return default_item
