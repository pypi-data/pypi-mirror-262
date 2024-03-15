import inspect
from .context import Nest, NestConfiguration, SnakeParameters


class Snake:
    def __init__(self, **kwargs):
        self.__snake_parameters = SnakeParameters(**kwargs)

    def __call__(self, class_definition):
        self.__snake_parameters.name = class_definition.__name__
        Nest.definition(class_definition, self.__snake_parameters)
        return class_definition


class Poisoned:

    def __init__(self, **kwargs):
        self.__config = kwargs

    def __call__(self, snake_method):
        def wrapper(*args, **kwargs):
            specs = inspect.getfullargspec(snake_method)
            args_list = specs[0]
            annotations = specs[6]
            real_args = []
            for i in range(len(args_list)):
                arg = args_list[i]

                if len(args) > i and args[i] is not None:
                    real_args.append(args[i])
                else:
                    real_args.append(Nest.inject(self.__config.get(arg, arg), annotations.get(arg)))

            return snake_method(*real_args, **kwargs)

        return wrapper


__all__ = ['Nest', 'NestConfiguration', 'Snake', 'Poisoned']
