"""
"""

import subprocess

def hasProgram(cmds):
    """
    """
    try:
        subprocess.call(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return False
    return True

class Builder(object):
    """
    """

    def __init__(self):
        """
        """
        raise NotImplementedError("Abstract constructor cannot be invoked")

    def exists(self):
        """Returns *True* if this builder can be used on this system
        """
        raise NotImplementedError("Abstract method cannot be invoked")

    def compile(self, srcPath, objPath):
        """Returns True if the compile operation was successful. Takes absolute
           path to a source file and absolute path to desired object file
           resulting from compilation.
        """
        raise NotImplementedError("Abstract method cannot be invoked")

    def linkExe(self, objPaths, exePath):
        """Links object files into a single standalone executable. Object
           files can include static libraries. Returns result of link operation
           (True or False).
        """
        raise NotImplementedError("Abstract method cannot be invoked")

    def linkLib(self, objPaths, libPath):
        """Links object files into a single static library. Returns result of
           link operation (True or False).
        """
        raise NotImplementedError("Abstract method cannot be invoked")
