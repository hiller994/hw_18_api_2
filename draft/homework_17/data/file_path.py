import os
from draft import homework_17


def path(file_name):
    return os.path.abspath(
        os.path.join(os.path.dirname(homework_17.tests.__file__), f'../data/{file_name}')
    )