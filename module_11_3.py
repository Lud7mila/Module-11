# интроспекция

import inspect
from pprint import pprint

def print_info(obj):
    '''Функция выводит на печать информацию об объекте'''
    print("\nobject: ", obj)
    pprint(introspection_info(obj), compact=True, sort_dicts=False)


class SomeClass:
    '''Класс SomeClass ещё в разработке.'''
    def __init__(self):
        self.attribute_1 = 27

    def some_class_method(self, value):
        self.attribute_1 = value
        print(self.attribute_1)


def introspection_info(obj):
    ''' Эта функция принимает объект (любого типа) в качестве аргумента и проводит интроспекцию этого объекта,
    чтобы определить его тип, атрибуты, методы, модуль, и другие свойства.'''
    obj_info = {}
    obj_info["type"] = type(obj)
    attrs = []
    methods = []
    [methods.append(attr_name) if callable(getattr(obj, attr_name)) else attrs.append(attr_name) for attr_name in dir(obj)]
    obj_info["attributes"] = attrs
    obj_info['methods'] = methods
    obj_info['module'] = inspect.getmodule(obj)
    obj_info['doc'] = obj.__doc__
    return obj_info


print_info(SomeClass)
print_info(SomeClass())
print_info(24)
print_info("Hello World!")
print_info(introspection_info)
print_info(inspect)
