"""
"""

import os
import re
import sys
import json
from epic import msvc

class Config(object):
    """
    """

    def __init__(self):
        """
        """
        self.arch = 64
        self.cfg = "Debug"

    def getStr(self):
        """
        """
        return "arch%u_cfg%s" % (self.arch, self.cfg)

class Package(object):
    """Package model encapsulates a specific directory to provide a transparent
       interface to specific file queries, etc.
    """

    def __init__(self, packPath):
        """
        """
        self.packPath = os.path.abspath(packPath)
        jsonPath = self.packPath + os.path.sep + "package.json"
        with open(jsonPath, 'r') as f:
            self.settings = json.load(f)

    def getHeaders(self):
        """Returns list of absolute paths to all .H files in the package.
        """
        headers = []
        for fileName in os.listdir(self.packPath):
            if fileName.lower().endswith(".h"):
                headers.append(self.packPath + os.path.sep + fileName)
        return headers

    def getSource(self):
        """Returns list of absolute paths to all .CPP files (that don't begin
           with "main_" or "test_") in the package.
        """
        source = []
        for fileName in os.listdir(self.packPath):
            if fileName.lower().endswith(".cpp") and not fileName.lower().startswith("main_") and not fileName.lower().startswith("test_"):
                source.append(self.packPath + os.path.sep + fileName)
        return source

    def getMains(self):
        """Returns list of absolute paths to all .CPP files that begin with
           "main_" in the package.
        """
        mains = []
        for fileName in os.listdir(self.packPath):
            if fileName.lower().endswith(".cpp") and fileName.lower().startswith("main_"):
                mains.append(self.packPath + os.path.sep + fileName)
        return mains

    def getTests(self):
        """Returns list of absolute paths to all .CPP files that begin with
           "test_" in the package.
        """
        tests = []
        for fileName in os.listdir(self.packPath):
            if fileName.lower().endswith(".cpp") and fileName.lower().startswith("test_"):
                tests.append(self.packPath + os.path.sep + fileName)
        return tests

    def getSemVer(self):
        """Returns a tuplet of (major,minor,patch) integers as defined by the
           semver in the top-most package folder
        """
        _, semver = os.path.split(self.packPath)
        parts = semver.split('.')
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])
        return major, minor, patch

    def getUNI(self):
        """Returns the UNI defined by name of the folder two levels up
           (top-most folder is semver), as period-delimited string.
        """
        dirPaths, _ = os.path.split(self.packPath)
        _, uni = os.path.split(dirPaths)
        return uni

    def getName(self):
        """Name is final part of UNI two folders up, assuming one folder up is
           semver.
        """
        uni = self.getUNI()
        return uni.split(".")[-1]

def getBuilder():
    """
    """
    if msvc.exists():
        return msvc
    else:
        raise Exception("No supported builders could be resolved")

def build(package):
    """
    """
    config = Config()
    builder = getBuilder()
    sources = package.getSource()
    mains = package.getMains()
    tests = package.getTests()
    objs = []
    for cpp in sources + mains + tests:
        fromPath = cpp
        _, fileName = os.path.split(cpp)
        name, _ = os.path.splitext(fileName)
        toPath = package.packPath + os.path.sep + "obj" + os.path.sep + config.getStr() + os.path.sep + name + ".obj"
        builder.compile(fromPath, toPath, defines=package.settings["defines"] if "defines" in package.settings else {})
        if cpp in sources:
            objs.append(toPath)
    libPath = package.packPath + os.path.sep + "lib" + os.path.sep + config.getStr() + os.path.sep + package.getName() + ".lib"
    builder.static(objs, libPath)
    for main in mains:
        _, fileName = os.path.split(main)
        objName, _ = os.path.splitext(fileName)
        exeName = re.sub("main_", "", objName)
        objPath = package.packPath + os.path.sep + "obj" + os.path.sep + config.getStr() + os.path.sep + objName + ".obj"
        toPath = package.packPath + os.path.sep + "bin" + os.path.sep + config.getStr() + os.path.sep + exeName + ".exe"
        fromPaths = [libPath, objPath]
        builder.executable(fromPaths, toPath)

def clean(package):
    """
    """
    pass

def doc(package):
    """
    """
    pass

def main(action, target):
    """
    """
    p = Package(target)
    if action == 'build':
        build(p)
    elif action == 'clean':
        clean(p)
    else:
        raise Exception("Unsupported epic action '%s'" % action)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Command-line invocation format: '> epic [action] [target?]'")
    action = sys.argv[1]
    if len(sys.argv) < 3:
        target = os.getcwd()
    else:
        target = sys.argv[2]
    main(action, target)
