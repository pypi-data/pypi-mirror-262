import inspect
import types
from .configuration import Configuration


class SnakeParameters:
    def __init__(self, **kwargs):
        self.__name = kwargs.get("name", None)
        self.__args = kwargs.get("args", None)
        self.__condition = kwargs.get("condition", None)
        self.__properties = kwargs.get("properties", None)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if self.__name is None:
            self.__name = name

    @property
    def args(self):
        return self.__args

    @args.setter
    def args(self, args):
        self.__args = args

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, condition):
        self.__condition = condition


class Context:
    __nest = None
    __exclude = ['self', 'cls']

    def __init__(self):
        Context.__init()

    @staticmethod
    def __init():
        if Context.__nest is None:
            Context.__nest = {'byQualifier': {}, 'byType': {}, 'definitions': {}}

    @staticmethod
    def __register_by_name(name, inst):
        Context.__nest['byQualifier'][name] = inst

    @staticmethod
    def __register_by_type(inst):
        type_list = inspect.getmro(type(inst))
        for type_name in type_list:
            if type_name is type(object()):
                continue

            if Context.__nest['byType'].get(type_name, None) is None:
                Context.__nest['byType'][type_name] = []

            Context.__nest['byType'][type_name].append(inst)

    @staticmethod
    def __get_class_by_name(name):
        return Context.__nest['byQualifier'].get(name, None)

    @staticmethod
    def __get_class_by_type(the_type):
        return Context.__nest['byType'].get(the_type, None)

    @staticmethod
    def __create_from_class(snake_class, snake_args):
        tmp_args = []
        args_specs = inspect.getfullargspec(snake_class.__init__)[0]
        for i in range(len(args_specs)):

            if args_specs[i] in Context.__exclude:
                continue

            tmp_args.append(snake_args.get(args_specs[i], None))

        return snake_class(*tmp_args)

    @staticmethod
    def __create_from_name(snake_name, snake_obj):
        snake_class = snake_obj[0]
        snake_args = snake_obj[1].args

        # update value from config
        if snake_args:
            for name, value in snake_args.items():
                snake_args[name] = Configuration.get(value, value)

        if type(snake_class) is not types.FunctionType:
            inst = Context.__create_from_class(snake_class, snake_args)
            Context.__register_by_name(snake_name, inst)
            Context.__register_by_type(inst)

    @staticmethod
    def __initialize_snakes():
        for snake_name, snake_value in Context.__nest['definitions'].items():
            Context.__create_from_name(snake_name, snake_value)

    @staticmethod
    def initialize():
        Context.__initialize_snakes()

    @staticmethod
    def clear():
        if Context.__nest is not None:
            Context.__nest.clear()
            del Context.__nest
            Context.__nest = None
            Context.__init()

    @staticmethod
    def definition(bean_definition, parameters: SnakeParameters):
        if not parameters.condition:
            Context.__nest['definitions'][parameters.name] = (bean_definition, parameters)
            return

        if Configuration.get(parameters.condition['key']) == parameters.condition['value']:
            Context.__nest['definitions'][parameters.name] = (bean_definition, parameters)

    @staticmethod
    def inject(name, the_type):
        inst = Context.__get_class_by_name(name)

        if inst:
            return inst

        inst_array = Context.__get_class_by_type(the_type)
        if inst_array and len(inst_array) > 1:
            raise Exception(f'too many instances of {str(the_type)}')
        elif inst_array:
            inst = inst_array[0]

        by_definitions = Context.__nest['definitions'].get(name, None)
        if not inst and by_definitions:
            return Context.__create_from_name(name, by_definitions)

        return inst


NestConfiguration = Configuration()
Nest = Context()
