"""Defines command line entry point for *epic* utilities.
"""

import sys
#from epic import builders, configs, packages

class Options(object):
    """Basic object for parsing and storing command-line options for both flags
       and key-value pairs
    """

    def __init__(self, argv, flags=None):
        """Parses the basic *sys.argv* list, with an optional declaration of
           flag (as opposed to key-value) arguments.
        """
        if flags is None:
            flags = []
        self.file = argv[0]
        self.flags = flags
        self.dict = {}
        for flag in flags:
            self.dict[flag] = False
        for arg in argv[1:]:
            parts = arg.split('=')
            if len(parts) is 1 and parts[0] in self.flags:
                self.dict[parts[0]] = True
            elif len(parts) is 2:
                self.dict[parts[0]] = parts[1]
            else:
                raise Exception('Unrecognized parameter "%s"' % parts[0])

def main(opts):
    """Primary entry point, utilizing an instance of the Options class as
       parsed from *sys.argv*.
    """
    print(opts)

if __name__ == "__main__":
    main(Options(sys.argv).dict)
