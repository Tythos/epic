"""
"""

from epic import operator

class MsvcLib(operator.Operator):
    """
    """

    def __init__(self):
        """
        """
        super(MsvcLib, self).__init__("lib", "archiving")

    def execute(self, inputs, output):
        """
        """
        args = ["lib", "/OUT:%s" % output, "/nologo"] + self.options + inputs
        self.runSubProc(args)
        
class LlvmLib(operator.Operator):
    """
    """

    def __init__(self):
        """
        """
        super(LlvmLib, self).__init__("llvm-lib", "archiving")

    def execute(self, inputs, output):
        """
        """
        args = ["llvm-lib", "/out:%s" % output] + self.options + inputs
        self.runSubProc(args)
