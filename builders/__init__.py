"""
"""

from epic.builders import msvc

def getBuilder():
    """
    """
    if msvc.exists():
        return msvc
    else:
        raise Exception("No supported builders could be resolved")
