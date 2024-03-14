import sys
import os.path

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader

class MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        print("Find Spec: {0}".format(fullname))
        return spec_from_loader(fullname, MyLoader(fullname))

class MyLoader(Loader):
    def __init__(self, name):
        self.ame = name

    def create_module(self, spec):
        return None # use default module creation semantics

    def exec_module(self, module):
        vars(module)['x'] = 'X'

def install():
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, MyMetaFinder())