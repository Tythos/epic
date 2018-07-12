"""Defines a set of methods for invoking MSVC components
"""

import os
import datetime
import subprocess

def _exists(cmd):
    """
    """
    try:
        p = subprocess.Popen([cmd, "/?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, _ = p.communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def _call(cmd, args):
    """Returns True or False depending on exceptions raised and contents of stderr
    """
    p = subprocess.Popen([cmd] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = p.communicate()
    except Exception:
        stderr = ' '
        stdout = ''
    if len(stderr) > 0:
        return False
    if stdout.find(": error ".encode("ascii")) < 0 and stdout.find(": fatal error ".encode("ascii")) < 0:
        return True
    return False
    
def _log(timestamp, event, description):
    """
    """
    print("[%s] %s: %s" % (timestamp.isoformat(), event.upper(), description.lower()))

def exists():
    """Needs *cl*, *link*, and *lib* to be exposed
    """
    return _exists("cl") and _exists("link") and _exists("lib")

def _getDepIncludes(package):
    """Returns a list of arguments for adding include paths for each package
       dependency. At this time, semver constraints are ignored and only the
       first directory in the UNI-level folder is included.
    """
    args = []
    for depPath in package.getDepPaths():
        args.append("/I" + depPath)
    return args

def _getDepLibs(package, config):
    """Returns a list of arguments for all library paths and .LIB files for
       each dependency listed in the package settings. This includes both
       /LIBPATH library paths and [package].LIB for the given build
       configuration. If the library file does not exist, a list of missing
       libraries is reported and an error is raised. (Future iterations may
       automatically recurse to build dependencies).
    """
    args = []
    libPaths = []
    for depPath in package.getDepPaths():
        libPath = depPath + os.path.sep + "lib" + os.path.sep + config.getStr()
        libPaths.append(libPath)
        args.append("/LIBPATH:" + libPath)
    missing = []
    if "dependencies" in package.settings:
        deps = package.settings["dependencies"].keys()
        for ndx, dep in enumerate(deps):
            libName = dep.split(".")[-1] + ".lib"
            libPath = libPaths[ndx] + os.path.sep + libName
            if not os.path.isfile(libPath):
                missing.append(libName)
            else:
                args.append(libName)
    if len(missing) > 0:
        for miss in missing:
            print(" > Static library '%s' could not be resolved" % miss)
        raise Exception("Missing dependency builds")
    return args

def compile(package, config, fromPath, toPath):
    """Given a package and configuration, executes the transformation that
       compiles source file at *fromPath* to object file at *toPath*. Includes
       paths for each dependency listed in package settings.
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    args = ["/c", "/nologo", "/EHsc", "/Fo" + toPath]
    if "defines" in package.settings:
        for k, v in package.settings["defines"].items():
            args += ["/D%s=%s" % (k, v)]
    if "dependencies" in package.settings:
        args += _getDepIncludes(package)
    result = _call("cl", args + [fromPath])
    _, fromFile = os.path.split(fromPath)
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", fromFile + " => " + toFile)

def static(package, config, fromPaths, toPath):
    """Given absolute paths to a collection of .OBJ files, archives them into a
       static library (.LIB).
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    result = _call("lib", ["/nologo", "/OUT:" + toPath] + fromPaths)
    fromFiles = [os.path.split(fromPath)[1] for fromPath in fromPaths]
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", "[" + ", ".join(fromFiles) + "] => " + toFile)

def executable(package, config, fromPaths, toPath):
    """Given absolute paths to a collection of .OBJ and .LIB files, links them
       into an executable. Includes library references (paths and files)
       for each dependency listed in the package settings.
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    depArgs = _getDepLibs(package, config)
    result = _call("link", ["/nologo", "/OUT:" + toPath] + depArgs + fromPaths)
    fromFiles = [os.path.split(fromPath)[1] for fromPath in fromPaths]
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", "[" + ", ".join(fromFiles) + "] => " + toFile)
