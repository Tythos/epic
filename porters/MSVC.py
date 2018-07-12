"""Porter interface for transforming package source and configuration to an
   MSVC solution/project.
"""

import random

MSVC_VERSION = "15.0.27130.0"
MSVC_MIN_VERSION = "10.0.40219.1"
MSVC_WIN_VERSION = "10.0.16299.0"

def getNewUUID():
    """DOES NOT ENFORCE EMBEDDED UUID VERSIONING
    """
    num = random.getrandbits(32 * 4)
    chars = "%032x" % num
    uuid = "%s-%s-%s-%s-%s" % (chars[:8], chars[8:12], chars[12:16], chars[16:20], chars[20:])
    return uuid

class Project(object):
    """
    """

    def __init__(self):
        """
        """
        self.uuid = getNewUUID()
        self.name = "untitled project"
        self.includePaths = []
        self.libraryPaths = []
        self.files = []
        self.libs = []

    def toFile(self, projPath):
        """
        """
        pass

    @classmethod
    def fromFile(cls, projPath):
        """
        """
        pass

class Solution(object):
    """
    """

    def __init__(self):
        """
        """
        self.uuid = getNewUUID()
        self.projects = []

    def toFile(self, slnPath):
        """
        """
        pass

    @classmethod
    def fromFile(cls, slnPath):
        """
        """
        pass

def main():
    """
    """
    pass

if __name__ == "__main__":
    main()
