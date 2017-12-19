"""Defines base class and variations, with utilities, for managing build
   configurations. A build configuration is used by a Builder subclass, which
   will interpret configurations in specific ways to modify/customize the build
   output. Base BuildConfig properties define options for architecture (32, 64)
   and variant (release, debug).

   BuildConfig objects are static; they do not exhibit active behaviors within
   the build chain but are instead read by Builder subclasses to customize
   compiler and linking options. Different builders will translate BuildConfig
   values into command line arguments or modified compiler/linker invocations
   in different ways.
"""

class BuildOption(object):
    """Encapsulates a single build option, including a name, list of supported
       options, and currently-selected value.
    """

    def __init__(self, options=None):
        """Initializes
        """
        if not options:
            raise Exception('Constructor requires a list of supported options')
        self.name = self.__class__.__name__
        self.options = options
        self.value = self.options[0]

    @classmethod
    def define(Cls, name, options):
        """Returns a new instance of the *BuildConfig* object with a specific
           name and options. Most build options don't need to subclass
           *BuildConfig*.
        """
        opt = Cls(options)
        opt.name = name
        return opt

class BuildConfig(object):
    """Defines a collection of build options, including their current values.
    """

    def __init__(self):
        """Basic build config model specifies architecture and variant options.
        """
        self.arch = BuildOption.define('arch', ['x86', 'x64'])
        self.variant = BuildOption.define('variant', ['debug', 'release'])
