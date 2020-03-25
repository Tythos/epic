"""
"""

from epic import operator

class MsvcLink(operator.Operator):
    """
    """

    def __init__(self):
        """
        """
        super(MsvcLink, self).__init__("link", "linking")

    def execute(self, inputs, output):
        """
        """
        args = ["link", "/OUT:%s" % output, "/nologo"] + self.options + inputs
        self.runSubProc(args)
