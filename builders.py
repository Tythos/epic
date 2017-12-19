"""Contains the base *Builder* class and basic MSVC and g++ builders. A
   *Builder* is the active agent in the build process that generates build
   products from a specific package and build configuration object.
"""

import subprocess

def safe_call(cmd, args=None):
    """Utilizes *subprocess.Popen* to safely call an external program.
    """
    if args is None:
        args = []
    all = [cmd] + args
    print(all)
    p = subprocess.Popen(all, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()

class Builder(object):
    """Models an abstract Builder with common properties and interfaces for
       compile and link operations.
    """

    def __init__(self):
        """Defines basic *Builder* model with empty parameters
        """
        self.compile_exe = ''
        self.link_exe = ''
        self.compile_args = []
        self.link_args = []

    def compile(self, target):
        """Defines compile process using *Builder* exe and flag properties
        """
        stdout, stderr = safe_call(self.compile_exe, self.compile_args + [target])
        if stderr:
            raise Exception('Encountered error at compile time: "%s"' % stderr)
        print(stdout)

    def link(self, targets):
        """Defines link process using *Builder* exe and flag properties
        """
        stdout, stderr = safe_call(self.link_exe, self.link_args + targets)
        if stderr:
            raise Exception('Encountered error at link time: "%s"' % stderr)
        print(stdout)

    def build(self, package, config):
        """Accepts a specific *Package* and *BuildConfig* object. Valid build
           targets within the package are compiled seperately, then linked
           together for each build product, in accordance with the specified
           build configuration.
        """
        pass

class MSVC(Builder):
    """Extends *Builder* to implement an interface to MSVC's command-line
       compiler and linker.
    """

    def __init__(self):
        """Defines MSVC command line properties
        """
        super(MSVC, self).__init__()
        self.compile_exe = 'cl.exe'
        self.link_exe = 'link.exe'
        self.compile_args = ['/EHsc', '/nologo', '/c']
        self.link_args = ['/nologo']

class GCC(Builder):
    """Extends *Builder* to implement an interface to g++
    """

    def __init__(self):
        """Defines GCC (g++) command line properties
        """
        super(GCC, self).__init__()
        self.compile_exe = 'g++'
        self.link_exe = 'g++'
        self.compile_args = ['-c']
        self.link_args = []
