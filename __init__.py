"""
"""

import os
import re
import json
import shutil
import datetime
import importlib
import subprocess
import params
from epic import builders, git

class Package(object):
    """
    """

    def __init__(self, absDir):
        """
        """
        self.absDir = os.path.abspath(absDir)

    def _getCfg(self):
        """Loads configuration information from package.json, if it exists. If
           it does not, an empty ("{}") config is written to file.
        """
        cfgPath = self.absDir + os.path.sep + "package.json"
        if not os.path.isfile(cfgPath):
            with open(cfgPath, "w") as f:
                f.write("{}")
        with open(cfgPath, "r") as f:
            cfg = json.load(f)
        return cfg

    def _getName(self):
        """Returns the package name (assumed to be folder name)
        """
        _, name = os.path.split(self.absDir)
        return name

    def _getFilteredContents(self, rep):
        """Returns a list of files in the root-level folder matching the given
           regexp pattern.
        """
        filtered = []
        for item in os.listdir(self.absDir):
            absPath = self.absDir + os.path.sep + item
            if os.path.isfile(absPath):
                if re.search(rep, item):
                    filtered.append(item)
        return filtered

    def init(self):
        """For current directory: add package.json; add .gitignore; add
           LICENSE; add README.
        """
        name = self._getName()
        with open(self.absDir + os.path.sep + "package.json", "w") as f:
            f.write("{}")
        with open(self.absDir + os.path.sep + ".gitignore", "w") as f:
            f.write("")
        with open(self.absDir + os.path.sep + "LICENSE", "w") as f:
            f.write("PROPRIETARY, EXOANALYTIC SOLUTIONS")
        with open(self.absDir + os.path.sep + "README.rst", "w") as f:
            f.write(name + "\n")
            f.write("=" * len(name))

    def buildDocs(self):
        """Publishes documentation from all source files into docs/, probably
           through doxygen.
        """
        pass

    def buildHeader(self):
        """Builds singular *include* header in current directory (maybe should
           be in inc/?). Aggregates all .h files in root-level folder, assuming
           each one has its own #ifndef checks where appropriate.
        """
        headerName = self._getName() + ".h"
        now = datetime.datetime.utcnow()
        lines = []
        lines.append("/* Automatic package header from epic")
        lines.append("   Generated " + now.strftime("%Y/%m/%d %H:%M:%S"))
        lines.append("*/")
        lines.append("")
        for header in self._getFilteredContents(r"\.h$"):
            if header == headerName:
                continue
            lines.append('#include "%s"' % header)
        lines.append("")
        headerPath = self.absDir + os.path.sep + headerName
        if False and os.path.isfile(headerPath):
            raise Exception("A header with the package name already exists")
        with open(headerPath, "w") as f:
            f.write("\n".join(lines))
        return headerPath

    def buildLib(self, builder):
        """Compiles all non-main, non-test .cpp files into a static library
        """
        cpp = set(self._getFilteredContents(r"\.cpp$"))
        main = set(self._getFilteredContents(r"^main_.+\.cpp$"))
        maintest = set(self._getFilteredContents(r"^main_test_.+\.cpp$"))
        test = set(self._getFilteredContents(r"^test_.+\.cpp$"))
        objFolder = self.absDir + os.path.sep + "obj"
        if not os.path.isdir(objFolder):
            os.mkdir(objFolder)
        objPaths = []
        for source in cpp - main - test - maintest:
            name, _ = os.path.splitext(source)
            srcPath = self.absDir + os.path.sep + source
            objPath = objFolder + os.path.sep + name + ".obj"
            builder.compile(srcPath, objPath)
            objPaths.append(objPath)
        libDir = self.absDir + os.path.sep + "lib"
        if not os.path.isdir(libDir):
            os.mkdir(libDir)
        libPath = libDir + os.path.sep + self._getName() + ".lib"
        builder.linkLib(objPaths, libPath)
        return libPath

    def buildTests(self, builder, skipLib=False):
        """Builds all test .cpp programs and places in bin/[arch]/[config].
           If *skipLib* isn't True, first builds header and lib.
        """
        if not skipLib:
            _ = self.buildHeader()
            libPath = self.buildLib(builder)
        else:
            libDir = self.absDir + os.path.sep + "lib"
            libPath = libDir + os.path.sep + self._getName() + ".lib"
        #cpp = set(self._getFilteredContents(r"\.cpp$"))
        #main = set(self._getFilteredContents(r"^main_.+\.cpp$"))
        maintest = set(self._getFilteredContents(r"^main_test_.+\.cpp$"))
        test = set(self._getFilteredContents(r"^test_.+\.cpp$"))
        objFolder = self.absDir + os.path.sep + "obj"
        if not os.path.isdir(objFolder):
            os.mkdir(objFolder)
        objPaths = []
        for source in test.union(maintest):
            name, _ = os.path.splitext(source)
            srcPath = self.absDir + os.path.sep + source
            objPath = objFolder + os.path.sep + name + ".obj"
            builder.compile(srcPath, objPath)
            objPaths.append(objPath)
        binDir = self.absDir + os.path.sep + "bin"
        if not os.path.isdir(binDir):
            os.mkdir(binDir)
        for objPath in objPaths:
            _, fileName = os.path.split(objPath)
            name, _ = os.path.splitext(fileName)
            exePath = binDir + os.path.sep + name + ".exe"
            builder.linkExe([objPath, libPath], exePath)

    def buildExes(self, builder, skipLib=False):
        """Builds all main .cpp programs and places in bin/[arch]/[config].
           Must first build header and lib to link against.
        """
        if not skipLib:
            _ = self.buildHeader()
            libPath = self.buildLib(builder)
        else:
            libDir = self.absDir + os.path.sep + "lib"
            libPath = libDir + os.path.sep + self._getName() + ".lib"
        #cpp = set(self._getFilteredContents(r"\.cpp$"))
        main = set(self._getFilteredContents(r"^main_.+\.cpp$"))
        maintest = set(self._getFilteredContents(r"^main_test_.+\.cpp$"))
        #test = set(self._getFilteredContents(r"^test_.+\.cpp$"))
        objFolder = self.absDir + os.path.sep + "obj"
        if not os.path.isdir(objFolder):
            os.mkdir(objFolder)
        objPaths = []
        for source in main - maintest:
            name, _ = os.path.splitext(source)
            srcPath = self.absDir + os.path.sep + source
            objPath = objFolder + os.path.sep + name + ".obj"
            builder.compile(srcPath, objPath)
            objPaths.append(objPath)
        binDir = self.absDir + os.path.sep + "bin"
        if not os.path.isdir(binDir):
            os.mkdir(binDir)
        for objPath in objPaths:
            _, fileName = os.path.split(objPath)
            name, _ = os.path.splitext(fileName)
            exePath = binDir + os.path.sep + name + ".exe"
            builder.linkExe([objPath, libPath], exePath)

    def clean(self):
        """Removes all contents of bin/, doc/, lib/, and obj/ folders.
        """
        for folder in ["bin", "doc", "lib", "obj"]:
            absFolder = self.absDir + os.path.sep + folder
            if os.path.isdir(absFolder):
                shutil.rmtree(absFolder)

def clone(uid):
    """UID consists of a server path, group name, and project name, all
       delimited by period. Will eventually need to support determination and
       checkout of appropriate tag from semver constraint, before it can be
       used to resolve package dependencies.
    """
    parts = uid.split(".")
    server = ".".join(parts[:-2][::-1])
    group = parts[-2]
    project = parts[-1]
    url = "https://%s/%s/%s.git" % (server, group, project)
    dest = os.environ["EPIC_LOCAL_REPO"] + os.path.sep + uid
    git.Repo.clone(url, dest)

def getDefaultBuilder():
    """Checks all modules in *buidlers* subfolder for classes of the same name
       that inherit from Builder. The first one that exists is the default.
    """
    builderPath = builders.__path__[0]
    for fileName in os.listdir(builderPath):
        modName, _ = os.path.splitext(fileName)
        absFile = os.path.abspath(builderPath + os.path.sep + fileName)
        if absFile.endswith(".py") and os.path.isfile(absFile):
            module = importlib.import_module("epic.builders." + modName)
            if hasattr(module, modName):
                cls = getattr(module, modName)
                if cls().exists():
                    return "epic.builders." + modName

def getBuilder(namespace):
    """A builder is identified by a namespace (module) in which a class exists
       that implements the Builder interface. Given that namespace, the class
       is returned. For example, the default Visual Studio builder has the
       namespace "epic.builders.MSVC", which would return an instance of the
       MSVC class from that module.
    """
    builderName = namespace.split(".")[-1]
    module = importlib.import_module(namespace)
    cls = getattr(module, builderName)
    return cls()

def main(root, action, arch, config, builder, uid):
    """
    """
    p = Package(root)
    b = getBuilder(builder)
    b.arch = arch
    b.config = config
    cfg = p._getCfg()
    if "defines" in cfg:
        b.defines = cfg["defines"]
    if action == "build":
        p.buildDocs()
        p.buildHeader()
        p.buildLib(b)
        p.buildTests(b)
        p.buildExes(b)
    elif action == "docs":
        p.buildDocs()
    elif action == "header":
        p.buildHeader()
    elif action == "lib":
        p.buildLib(b)
    elif action == "tests":
        p.buildTests(b)
    elif action == "exes":
        p.buildExes(b)
    elif action == "clean":
        p.clean()
    elif action == "clone":
        clone(uid)
    elif action == "init":
        p.init()
    else:
        raise Exception("Unsupported action '%s'" % action)

if __name__ == "__main__":
    p = params.Params()
    action = p.optional("action", "all") #action = p.required("action")
    root = p.optional("root", ".") #root = p.required("root")
    arch = p.optional("arch", "64")
    config = p.optional("config", "debug")
    builder = p.optional("builder", getDefaultBuilder())
    uid = p.optional("uid", None)
    main(root, action, arch, config, builder, uid)
