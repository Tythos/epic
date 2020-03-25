"""
"""

import subprocess

class Operator(object):
    """An operator object is responsible for performing a command-line
       execution that transforms one or more inputs into a single output
       resource, using a particular configuration.
    """
    
    def __init__(self, cmdExe=None, actTerm=""):
        """
        """
        self.cmdExe = cmdExe
        self.actTerm = actTerm
        self.options = []

    def runSubProc(self, args):
        """
        """
        sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = sp.communicate()
        if 0 < sp.returncode:
            print(stdout.decode("ascii", errors="ignore"))
            raise Exception("Subprocess %s failed while %s (see above)" % (str(args), self.actTerm))

    def execute(self, inputs, output):
        """
        """
        raise NotImplementedError()

    def assertExists(self):
        """
        """
        sp = subprocess.Popen(self.cmdExe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = sp.communicate()
        except FileNotFoundError:
            raise Exception("Operator command '%s' could not be resolved" % self.cmdExe)
