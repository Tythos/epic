"""
"""

from epic.ides import msvc

def getIde():
    """
    """
    if msvc.exists():
        return msvc
    else:
        raise Exception("No supported IDEs could be resolved")
