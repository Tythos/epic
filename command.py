"""Defines command line entry point for *epic* utilities.
"""

import os
import sys
import importlib
import subprocess
from epic import builders, configs, packages

class Params(object):
    """Basic object for parsing and storing command-line options for both flags
       and key-value pairs
    """

    def __init__(self, argv):
        """Parses the basic *sys.argv* list for epic command arguments. The
           *argv* list will have:
           #. The name of this file (command.py) as invoked to Python
           #. The desired action, as specified by the user
           #. Any option "key=value" pairs (0 or more)
           #. An action target (path), defaulting to the CWD

           The action and target are stored in *action* and *target* fields.
           All others ("key=value" pairs) are stored in the *options* dict.
        """
        self.action = ''
        self.target = os.getcwd()
        self.options = {}
        if len(argv) < 2:
            raise Exception('An action is required')
        for ndx, arg in enumerate(argv):
            parts = arg.split('=')
            if ndx is 0:
                continue
            elif ndx is 1:
                self.action = arg
            elif len(parts) is 2:
                self.options[parts[0]] = parts[1]
            elif ndx == len(argv) - 1:
                self.target = os.path.abspath(arg)
            else:
                raise Exception('Intermediate arguments must have "key=value" form')

    def __str__(self):
        """Returns a string representation of the Options object that includes
           a listing of options and other parameters
        """
        header = '<%s.%s object at 0x%x>' % (self.__class__.__module__, self.__class__.__name__, id(self))
        action = '\taction: %s' % self.action
        target = '\ttarget: %s' % self.target
        options = []
        for k, v in self.options.iteritems():
            options.append('\t%s: %s' % (k, v))
        return '\n'.join([header, action, target] + options)

class ActionRoutes:
    """Organizes supported action routes for command-line invocation
    """

    @staticmethod
    def build(self, params):
        """Assembles the appropriate builder, which is then invoked to compile
           and link all artifacts in the given package. If no builder is
           specified, we default to g++/MSVC (in that order). If no config is
           specified, we default to BuildConfig (variant=debug, arch=x86).
        """
        if 'builder' in params.options:
            cls = resolveModel(params.options['builder'])
            b = cls()
        else:
            g = builders.GCC()
            m = builders.MSVC()
            if g.isExists():
                b = g
            elif m.isExists():
                m = g
            else:
                raise Exception('Unable to resolve a supported Builder')
        p = packages.Package(params.target)
        if 'config' in params.options:
            cls = resolveModeL(params.options['config'])
            c = cls()
        else:
            c = configs.BuildConfig()
        b.build(p, c)

def resolveModel(modelPath):
    """Given a model path (module + class name), uses *importlib* in an attmept
       to load that class symbol and return it. An exception will be raised if
       the module does not exist or the class is not present.
    """
    try:
        parts = modelPath.split('.')
        modulePath = '.'.join(parts[:-1])
        className = parts[-1]
        module = importlib.import_module(modulePath)
        return getattr(module, className)
    except Exception as e:
        raise Exception('Invalid model path "%s"' % modelPath)

def main(params):
    """Primary entry point, utilizing an instance of the Options class as
       parsed from *sys.argv*. This mainly consists of determining the
       appropriate action from *ActionRoutes*.
    """
    if not hasattr(ActionRoutes, params.action):
        raise Exception('"%s" is not a supported action' % params.action)
    method = getattr(ActionRoutes, params.action)
    method(params)

if __name__ == "__main__":
    main(Params(sys.argv))

