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
    if stdout.find(': error '.encode('ascii')) < 0:
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

def compile(fromPath, toPath, **kwargs):
    """
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    args = ["-c", "/nologo", "/EHsc", "/Fo" + toPath]
    if "defines" in kwargs:
        for k, v in kwargs["defines"].items():
            args += ["/D%s=%s" % (k, v)]
    result = _call("cl", args + [fromPath])
    _, fromFile = os.path.split(fromPath)
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", fromFile + " => " + toFile)

def static(fromPaths, toPath):
    """Given absolute paths to a collection of .OBJ files, archives them into a
       static library (.LIB)
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    result = _call("lib", ["/nologo", "/OUT:" + toPath] + fromPaths)
    fromFiles = [os.path.split(fromPath)[1] for fromPath in fromPaths]
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", "[" + ", ".join(fromFiles) + "] => " + toFile)

def dynamic(fromPaths, toPath):
    """
    """
    raise NotImplementedError("MSVC builder has not yet implemented dynamic library build")

def executable(fromPaths, toPath):
    """Given absolute paths to a collection of .OBJ and .LIB files, links them
       into an executable
    """
    toDir, _ = os.path.split(toPath)
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    result = _call("link", ["/nologo", "/OUT:" + toPath] + fromPaths)
    fromFiles = [os.path.split(fromPath)[1] for fromPath in fromPaths]
    _, toFile = os.path.split(toPath)
    _log(datetime.datetime.now(), "success" if result else "failure", "[" + ", ".join(fromFiles) + "] => " + toFile)
