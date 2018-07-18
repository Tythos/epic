"""
"""

from epic.ides import msvc

def main():
    """
    """
    sln = msvc.Solution()
    sln.name = 'proj1'
    proj1 = msvc.Project()
    proj1.name = 'proj1'
    proj1.includePaths = ['one\\inc']
    proj1.libraryPaths = ['one\\lib']
    proj1.intDir = 'obj'
    proj1.outDir = 'bin'
    proj1.libraryFiles = ['one.lib']
    proj1.headers = ['one.h']
    proj1.sources = ['one.cpp']
    proj1.buildType = 'StaticLibrary'
    sln.projects.append(proj1)
    proj2 = msvc.Project()
    proj2.name = 'proj2'
    proj2.includePaths = ['two\\inc']
    proj2.libraryPaths = ['two\\lib']
    proj2.intDir = 'obj'
    proj2.outDir = 'bin'
    proj2.libraryFiles = ['two.lib']
    proj2.headers = ['two.h']
    proj2.sources = ['two.cpp']
    proj2.buildType = 'Application'
    sln.projects.append(proj2)
    sln.save("test\\test.sln")

if __name__ == "__main__":
    main()
