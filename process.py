"""Common process model
"""

class Process(object):
    """Models a process that consumes multiple input files with a specific
       configuration. A builder The process translates these into system commands that
       are then invoked to generate an output file.
    """

    def __init__(self):
        """A process has four properties: input files; configuration; system
           commands; and output files.
        """
        self.inputs = []
        self.config = {}
        self.commands = []
        self.outputs = []
