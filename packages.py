"""
"""

import os
import json

class Package(object):
    """Models a package based on a specific path. For the most part this is a
        passive model that provides the Builder with a common interface for
        investigating package properties and organizing contents.
    """

    def __init__(self, path):
        """Initializes a package model from a specific path, loading
           *epic.json* at the package root if it exists and defining an empty
           one if it does not.
        """
        self.path = os.path.abspath(path)
        cfg_path = self.path + os.path.sep + 'epic.json'
        if os.path.isfile(cfg_path):
            with open(cfg_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {'dependencies': []}
            with open(cfg_path, 'w') as f:
                json.dump(self.config, f, indent=4)

    def getSource(self):
        """Returns a list of all source (*.cpp) files to be compiled into a
           static library for this package. Does NOT include .cpp files that
           begin with "main_" or "test_".
        """
        pass

    def getMain(self):
        """Returns a list of all main .cpp source files in this package folder.
           These are all .cpp files that begin with "main_", as well as
           "main.cpp" (if it exists).
        """
        pass

    def getTest(self):
        """Returns a list of all test .cpp source files in this package folder.
           These are all .cpp files that begin with "test_", as well as
           "test.cpp" (if it exists).
        """
        pass

    def getOutName(self, file):
        """Returns the output name of the given file, which can have one of
           four possible formats:
           #. "main.cpp" is the primary entry point for this package. In this
              case, the package name is returned.
           #. "main_(...).cpp" is a secondary entry point for this package. In
              this case, the name in (...) is returned.
           #. "test.cpp" is the primary test case for this package. In this
              case, the package name is returned.
           #. "test_(...).cpp" is a secondary test case for this package. In
              this case, the name in (...) is returned.

           Output names will be used to determine the binary executable that
           results from linking that compiler result against the package static
           library. Entry points will be send to "bin/" while test cases will
           be sent to "test/".
        """
	pass

    def cleanPaths(self):
        """Removes all entries from the intermediate and output folders *obj*
           and *bin*, respectively.
        """
        pass

    def getObjPath(self):
        """Returns the absolute path to the *obj* folder in the package.
           Creates the folder, if it does not already exist.
        """
        objPath = self.path + os.path.sep + 'obj'
        if not os.path.isdir(objPath):
            os.mkdir(objPath)
        return objPath

    def getBinPath(self):
        """Returns absolute path to the *bin* folder in the package
        """
        binPath = self.path + os.path.sep + 'bin'
        if not os.path.isdir(binPath):
            os.mkdir(binPath)
        return binPath

