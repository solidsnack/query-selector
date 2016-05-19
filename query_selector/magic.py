import sys
from types import ModuleType

from stackclimber import stackclimber

from . import QuerySelector


def auto(name):
    name = name.__name__ if isinstance(name, ModuleType) else name
    if name in sys.modules:
        pkg, resource = name.rsplit('.', 1)
        return QuerySelector((pkg, resource + '.sql'))
    else:                                                 # Must be in a script
        path = (name[:-3] if name.endswith('.py') else name) + '.sql'
        with open(path) as h:
            return QuerySelector(h)


# This is how we overload `import`. Modelled on Andrew Moffat's `sh`.
class ImportWrapper(ModuleType):
    def __init__(self, module):
        self._module = module

        # From the original -- these attributes are special.
        for attr in ['__builtins__', '__doc__', '__name__', '__package__']:
            setattr(self, attr, getattr(module, attr, None))

        # Path settings per original -- seemingly obligatory.
        self.__path__ = []

    def __getattr__(self, name):
        if name == 'queries':
            return auto(stackclimber(1))
        return getattr(self._module, name)


self = sys.modules[__name__]
sys.modules[__name__] = ImportWrapper(self)
