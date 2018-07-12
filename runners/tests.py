"""
"""

import os

def build(package, builder, skipLib=False):
    """Builds all test .cpp programs and places in bin/[arch]/[config].
        If *skipLib* isn't True, first builds header and lib.
    """
    if not skipLib:
        _ = package.buildHeader()
        libPath = package.buildLib(builder)
    else:
        libDir = package.absDir + os.path.sep + "lib"
        libPath = libDir + os.path.sep + package._getName() + ".lib"
    #cpp = set(self._getFilteredContents(r"\.cpp$"))
    #main = set(self._getFilteredContents(r"^main_.+\.cpp$"))
    maintest = set(package._getFilteredContents(r"^main_test_.+\.cpp$"))
    test = set(package._getFilteredContents(r"^test_.+\.cpp$"))
    objFolder = package.absDir + os.path.sep + "obj"
    if not os.path.isdir(objFolder):
        os.mkdir(objFolder)
    objPaths = []
    for source in test.union(maintest):
        name, _ = os.path.splitext(source)
        srcPath = package.absDir + os.path.sep + source
        objPath = objFolder + os.path.sep + name + ".obj"
        builder.compile(srcPath, objPath)
        objPaths.append(objPath)
    binDir = package.absDir + os.path.sep + "bin"
    if not os.path.isdir(binDir):
        os.mkdir(binDir)
    for objPath in objPaths:
        _, fileName = os.path.split(objPath)
        name, _ = os.path.splitext(fileName)
        exePath = binDir + os.path.sep + name + ".exe"
        builder.linkExe([objPath, libPath], exePath)
