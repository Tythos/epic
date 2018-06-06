"""
"""

import subprocess
from epic import builders

class MSVC(builders.Builder):
    """Defines a programmatic interface to the MSVC compiler/linker
    """
    
    def __init__(self):
        """
        """
        self.arch = ""
        self.config = ""

    def exists(self):
        """
        """
        return builders.hasProgram(["cl"]) and builders.hasProgram(["link", "/TIME"]) and builders.hasProgram(["lib"])

    def compile(self, srcPath, objPath):
        """Returns True if the compile operation was successful. Takes absolute
           path to a source file and absolute path to desired object file
           resulting from compilation.
        """
        p = subprocess.Popen(["cl", "/c", "/Fo"+objPath, "/nologo", srcPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if len(out) < 0 or len(err) < 0:
            # can process/parse output/error for future extraction
            return False
        return True

    def linkLib(self, objPaths, libPath):
        """Links object files into a single static library. Returns result of
           link operation (True or False).
        """
        p = subprocess.Popen(["lib", "/nologo", "/OUT:"+libPath] + objPaths, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if len(out) < 0 or len(err) < 0:
            # can process/parse output/error for future extraction
            return False
        return True

    def linkExe(self, objPaths, exePath):
        """Links object files into a single standalone executable. Object
           files can include static libraries. Returns result of link operation
           (True or False).
        """
        p = subprocess.Popen(["link", "/nologo", "/OUT:"+exePath] + objPaths, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if len(out) < 0 or len(err) < 0:
            # can process/parse output/error for future extraction
            return False
        return True
