"""
"""

import os

def build(package, builder):
    """Compiles all non-main, non-test .cpp files into a static library
    """
    cpp = set(package._getFilteredContents(r"\.cpp$"))
    main = set(package._getFilteredContents(r"^main_.+\.cpp$"))
    maintest = set(package._getFilteredContents(r"^main_test_.+\.cpp$"))
    test = set(package._getFilteredContents(r"^test_.+\.cpp$"))
    objFolder = package.absDir + os.path.sep + "obj"
    if not os.path.isdir(objFolder):
        os.mkdir(objFolder)
    objPaths = []
    for source in cpp - main - test - maintest:
        name, _ = os.path.splitext(source)
        srcPath = package.absDir + os.path.sep + source
        objPath = objFolder + os.path.sep + name + ".obj"
        builder.compile(srcPath, objPath)
        objPaths.append(objPath)
    libDir = package.absDir + os.path.sep + "lib"
    if not os.path.isdir(libDir):
        os.mkdir(libDir)
    libPath = libDir + os.path.sep + package._getName() + ".lib"
    builder.linkLib(objPaths, libPath)
    return libPath
