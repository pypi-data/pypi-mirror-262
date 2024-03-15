from .rulez import Rulez


class Configuration:
    __rulez = None

    def __init__(self):
        # print(environ)
        Configuration.__rulez = Rulez('nest.yaml')

    @staticmethod
    def get(key, default=None):
        return Configuration.__rulez.get(key, default)
