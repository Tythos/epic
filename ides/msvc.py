"""
"""

import uuid

class Solution(object):
    """
    """
    
    def __init__(self):
        """
        """
        self.uuid = str(uuid.uuid4())
        self.projects = []

    def save(self, slnPath):
        """
        """
        lines = []
        lines.append("Microsoft Visual Studio Solution File, Format Version 12.00")
        lines.append("VisualStudioVersion = 14.0.25420.1")
        lines.append("MinimumVisualStudioVersion = 10.0.40219.1")
        for project in self.projects:
            projPath = r"%s\%s.vcxproj" % (project.name, project.name)
            args = (self.id, project.name, projPath, project.id)
            lines.append("Project(\"{%s}\") = \"%s\", \"%s\", \"{%s}\"" % args)
            lines.append("EndProject")
            self.project.save(projPath)
        with open(slnPath, 'w') as f:
            f.writelines('\n'.join(lines))

class Project(object):
    """
    """
    pass

def export(package, destPath):
    """Given a particular package and destination path, writes a solution
       consisting of a project for the library and each link target.
    """
    pass
