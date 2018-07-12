"""
"""

import os
import re
import sys
import json
import shutil
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
        if not os.path.isfile(jsonPath):
            with open(jsonPath, 'w') as f:
                json.dump({}, f)
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
            if fileName.lower().endswith(".cpp") and not fileName.lower().startswith("main_") and not fileName.lower().startswith("test_") and not fileName.lower() == "main.cpp":
                source.append(self.packPath + os.path.sep + fileName)
        return source

    def getMains(self):
        """Returns list of absolute paths to all .CPP files that begin with
           "main_" in the package. Also checks for "main.cpp".
        """
        mains = []
        for fileName in os.listdir(self.packPath):
            if fileName.lower().endswith(".cpp") and fileName.lower().startswith("main_"):
                mains.append(self.packPath + os.path.sep + fileName)
        mainPath = self.packPath + os.path.sep + "main.cpp"
        if os.path.isfile(mainPath):
            mains.append(mainPath)
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

    def assertDependencies(self):
        """Uses listings in *dependencies* property of *package.json* settings
           to verify those UNIs are available on the current system. Otherwise,
           reports each unavailable dependency and throws an error. At this
           time, does not verify semver constraints. Packages must exist within
           the path indicated by the *EPIC_LOCAL_REPO* environmental variable.
        """
        elr = os.path.abspath(os.environ["EPIC_LOCAL_REPO"])
        if "dependencies" not in self.settings:
            return
        missing = []
        for dep, _ in self.settings["dependencies"].items():
            packPath = elr + os.path.sep + dep
            if not os.path.isdir(packPath):
                missing.append(dep)
        if len(missing) > 0:
            for uni in missing:
                print(" > Dependency '%s' not found" % uni)
            raise Exception("Missing dependencies")

    def getDepPaths(self):
        """Returns a list of absolute paths to all dependencies of the package.
           Currently ignores semver constraints and only includes the first
           subfolder within the UNI directory.
        """
        if "dependencies" not in self.settings:
            return []
        elr = os.path.abspath(os.environ["EPIC_LOCAL_REPO"])
        depPaths = []
        for dep, _ in self.settings["dependencies"].items():
            uniPath = elr + os.path.sep + dep
            depPath = None
            for item in os.listdir(uniPath):
                absPath = uniPath + os.path.sep + item
                if os.path.isdir(absPath):
                    depPath = absPath
                    break
            if depPath is None:
                raise Exception("Could not resolve semver folder within package directory for '%s'" % dep)
            depPaths.append(depPath)
        return depPaths

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
    package.assertDependencies()
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
        builder.compile(package, config, fromPath, toPath)
        if cpp in sources:
            objs.append(toPath)
    libPath = package.packPath + os.path.sep + "lib" + os.path.sep + config.getStr() + os.path.sep + package.getName() + ".lib"
    builder.static(package, config, objs, libPath)
    for main in mains:
        _, fileName = os.path.split(main)
        objName, _ = os.path.splitext(fileName)
        exeName = package.getName() if objName == "main" else re.sub("main_", "", objName)
        objPath = package.packPath + os.path.sep + "obj" + os.path.sep + config.getStr() + os.path.sep + objName + ".obj"
        toPath = package.packPath + os.path.sep + "bin" + os.path.sep + config.getStr() + os.path.sep + exeName + ".exe"
        fromPaths = [libPath, objPath]
        builder.executable(package, config, fromPaths, toPath)

def clean(package):
    """Deletes (including contents and subfolders) the following folders:
        * bin
        * lib
        * obj
    """
    shutil.rmtree(package.packPath + os.path.sep + 'bin')
    shutil.rmtree(package.packPath + os.path.sep + 'lib')
    shutil.rmtree(package.packPath + os.path.sep + 'obj')

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
