"""
"""

import os
import shutil
from epic import actors

class MsvcCl(actors.Actor):
    """
    """

    def __init__(self):
        """
        """
        super(MsvcCl, self).__init__("cl", "compiling")

    def execute(self, inputs, output):
        """
        """
        args = ["cl", "/c", "/EHsc", "/nologo", "/Fo:%s" % output, inputs[0]] + self.options
        self.runSubProc(args)
        extless, ext = os.path.splitext(inputs[0])
        initout = extless + ".obj" # what was generated (/OUT: is deprecated)
        #shutil.move(initout, output)

class LlvmClangpp(actors.Actor):
    """
    """

    def __init__(self):
        """
        """
        super(LlvmClangpp, self).__init__("clang++", "compiling")

    def execute(self, inputs, output):
        """
        """
        args = ["clang++", "-c", "-o", output] + self.options + [inputs[0]]
        self.runSubProc(args)
