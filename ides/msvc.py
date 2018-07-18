"""
"""

import os
import uuid
import pybars

def getTemplate(format):
    """
    """
    hbsPath = __file__.replace('.py', '.%s.hbs' % format)
    with open(hbsPath, 'r') as f:
        template = pybars.Compiler().compile(f.read())
    return template

class Solution(object):
    """
    """
    
    def __init__(self):
        """
        """
        self.uuid = str(uuid.uuid4())
        self.name = ''
        self.projects = []

    def save(self, slnPath):
        """Saves a solution, including child projects, to a specific solution
           path (file) and subfolders for each project.
        """
        tmpl = getTemplate('sln')
        projectFields = []
        slnDir, _ = os.path.split(slnPath)
        if not os.path.isdir(slnDir):
            os.makedirs(slnDir)
        for proj in self.projects:
            relProjPath = r"%s\%s.vcxproj" % (proj.name, proj.name)
            absProjPath = slnDir + os.path.sep + relProjPath
            projectFields.append({
                'slnUuid': self.uuid,
                'name': proj.name,
                'path': relProjPath,
                'uuid': proj.uuid
            })
            proj.save(absProjPath)
        with open(slnPath, 'w') as f:
            f.write(tmpl({'projectFields': projectFields}))

class Project(object):
    """
    """
    
    def __init__(self):
        """NOTE: File paths indicated by headers and sources are prepended
           within the template by two-up relative directory. That assumes the
           folder structure looks something like:
              / EPIC package (including .cpp, .h)
                 / msvc (including solution)
                    / [project] (from which headers, sources are referenced)
        """
        self.uuid = str(uuid.uuid4())
        self.name = ''
        self.includePaths = []
        self.libraryPaths = []
        self.intDir = ''
        self.outDir = ''
        self.libraryFiles = []
        self.headers = []
        self.sources = []
        self.buildType = 'Application'

    def save(self, projPath):
        """Writes a project file to a specific file path, including a filters
           definition file (colocated in the same folder).
        """
        vcxprojTemplate = getTemplate('vcxproj')
        filterTemplate = getTemplate('filters')
        fields = {
            'uuid': self.uuid,
            'name': self.name,
            'includePaths': ';'.join(self.includePaths),
            'libraryPaths': ';'.join(self.libraryPaths),
            'intDir': self.intDir,
            'outDir': self.outDir,
            'libraryFiles': ';'.join(self.libraryFiles),
            'headers': self.headers,
            'sources': self.sources,
            'buildType': self.buildType
        }
        projDir, _ = os.path.split(projPath)
        if not os.path.isdir(projDir):
            os.mkdir(projDir)
        with open(projPath, 'w') as f:
            f.write(vcxprojTemplate(fields))
        with open(projPath + ".filters", 'w') as f:
            f.write(filterTemplate(fields))

def export(package, destPath):
    """Given a particular package and destination path, writes a solution
       consisting of a project for the library and each link target. For the
       particular package, this means first defining the solution and project
       models to be exported, then saving them to files.
    """
    pass
