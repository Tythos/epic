"""Primary interaction point for epic behaviors, including logical models.
"""

import os
import csv
import sys
import datetime
from epic import compilers, linkers, archivers

EPIC_PATH, _ = os.path.split(os.path.abspath(__file__))

class BuildGraph(object):
    """Encapsulates a set of vertices and edges determined by a build_graph.csv
       table provided to the constructor. Also stores operator configurations,
       which default to MSVC compiler/linker/archiver commands. Uses a RAII
       pattern explicitly tied to a specific build graph table (.CSV file),
       whose entries (edges) are loaded at instantiation. These can be written
       back to the same file using the save() method, and an empty build graph
       will be created if one does not exist at that path.
    """

    def __init__(self, buildGraphPath):
        """The build graph is defined by a set of vertices (artifacts) and edges
           (operations). Edges are defined in the build_graph.csv table, while vertices
           are backed out from those entries. Those vertices can be organized into
           three sets:

           * Vertices listed as "from" but not "to" are source artifacts. These
             should always be present and will never be modified by the build
             process.

           * Vertices listed as both "from" and "to" are intermediate artifacts.
             These may or may not be present at any given point in time, and will
             be generated by various operations in the build process.

           * Vertices listed as only "to" are final artifacts (build products).
             These may or may not be present at any given point in time, and will
             be generated by final operations in the build process.

           Intermediate and final artifacts can have more than one predecessor
           (edge leading to that vertex). Common examples might include
           multiple object files being archived into a static library.
           
           This constructor initializes the object with a list of vertices
           (file name strings) and edges (rows from the CSV, as a list of
           dictionaries).
        """
        self.buildGraphPath = os.path.abspath(buildGraphPath)
        if not os.path.isfile(self.buildGraphPath):
            # create empty build graph table at path
            with open(self.buildGraphPath, 'w') as f:
                dw = csv.DictWriter(f, fieldnames=["from", "action", "to"], lineterminator="\n")
                dw.writeheader()
        with open(self.buildGraphPath, 'r') as f:
            dr = csv.DictReader(f)
            self.edges = [row for row in dr]
        self.operators = { # default names of operator modules
            "compiler": compilers.MsvcCl, # cpp=>obj
            "linker": linkers.MsvcLink, # obj=>exe
            "archiver": archivers.MsvcLib # obj=>lib
        }

    def getProjectPath(self):
        """Returns absolute path to the folder where the build graph file is
           located.
        """
        projPath, _ = os.path.split(self.buildGraphPath)
        return projPath

    def save(self):
        """Writes the build graph out to the path
        """
        with open(self.buildGraphPath, 'w') as f:
            dw = csv.DictWriter(f, fieldnames=["from", "action", "to"], lineterminator="\n")
            dw.writeheader()
            dw.writerows(self.edges)

    def getVertices(self):
        """
        """
        froms = [e["from"] for e in self.edges]
        tos = [e["to"] for e in self.edges]
        return list(set(froms + tos))

    def assertTools(self):
        """Raises an exception if the cmdExe does not exist for each operator
           currently in the build graph configuration
        """
        for key in self.operators.keys():
            self.operators[key].assertExists()

    def getSourceVertices(self):
        """Returns list of all vertices that do not have predecessors.
        """
        sources = []
        vertices = self.getVertices()
        for v in vertices:
            froms = [e for e in self.edges if e["from"] == v]
            tos = [e for e in self.edges if e["to"] == v]
            if len(froms) == 0:
                sources.append(v)
        return sources

    def getIntermediateVertices(self):
        """Returns a list of all intermediate vertices (build products), as
           determined by those with both "to" and "from edge connections.
        """
        intermediates = []
        vertices = self.getVertices()
        for v in vertices:
            froms = [e for e in self.edges if e["from"] == v]
            tos = [e for e in self.edges if e["to"] == v]
            if 0 < len(tos) and 0 < len(froms):
                intermediates.append(v)
        return intermediates

    def getFinalVertices(self):
        """Analyzes edges to determine which vertices are listed only as "to".
        """
        finals = []
        vertices = self.getVertices()
        for v in vertices:
            froms = [e for e in self.edges if e["from"] == v]
            tos = [e for e in self.edges if e["to"] == v]
            if len(froms) == 0 and 0 < len(tos):
                finals.append(v)
        return finals

    def getEdgesTo(self, to):
        """Returns the operations (edges) that generate the given to (vertex).
        """
        return [e for e in self.edges if e["to"] == to]

    def traverse(self, v, level=0):
        """For a given vertex, recurses to "from" vertices for the generating
           operation (if this vertex is not a source artifact). Then,
           determines if it must be re-generated by it's corresponding edge
           operation by comparision of "from" date modified against "to" date
           modified.
        """
        print("".join(["\t"] * level) + v)
        ei = self.getEdgesTo(v)
        if len(ei) == 0:
            # source artifact; degenerate case
            return
        # assert same operation for each edge
        oi = [e["action"] for e in ei]
        assert len(set(oi)) == 1, "Vertex %s must be generated by identical edge operations" % v
        vi = [e["from"] for e in ei]
        # recurse to edge "froms"
        fromDts = []
        for v_ in vi:
            # check source nodes--recurse, determine mod date
            self.traverse(v_, level+1)
            fullPath = os.path.abspath(self.getProjectPath() + "/%s" % v_)
            dateMod = datetime.datetime.fromtimestamp(os.path.getmtime(fullPath))
            fromDts.append(dateMod)
        # compare "from" dates against "to" dates (assuming it exists)
        fullPath = os.path.abspath(self.getProjectPath() + "/%s" % v)
        isExists = os.path.isfile(fullPath)
        isRebuildNeeded = not isExists
        # rebuild is needed if any source artifacts have been modified after this vertex
        if isExists:
            toDt = datetime.datetime.fromtimestamp(os.path.getmtime(fullPath))
            isRebuildNeeded = any([toDt < dt for dt in fromDts])
        else:
            # create folder if it also doesn't exist
            toPath, _ = os.path.split(fullPath)
            if not os.path.isdir(toPath):
                os.makedirs(toPath)
        if isRebuildNeeded:
            self.buildVertex(v, ei)

    def buildVertex(self, v, ei):
        """Executes an operation to build the given vertex. This is mainly
           branching logic to specific "operator" functions.
        """
        # assert same operation for each edge
        oi = [e["action"] for e in ei]
        assert len(set(oi)) == 1, "Vertex %s must be generated by identical edge operations" % v
        vi = [e["from"] for e in ei]
        operation = oi[0]
        operator = None
        if operation == "compile":
            # compiler operations should be 1-to-1
            assert len(vi) == 1, "Compile operations are 1-to-1 transformations ('%s')" % v
            operator = self.operators["compiler"]()
        elif operation == "link":
            # linker operations can be n-to-1
            operator = self.operators["linker"]()
        elif operation == "archive":
            # archive operations can be n-to-1
            operator = self.operators["archiver"]()
        else:
            raise Exception("Unsupported operation '%s' to generate artifact '%s'" % (operation, v))
        # adjust paths of vertices to project root
        operator.execute([
            os.path.abspath(self.getProjectPath() + "/" + i) for i in vi
        ], os.path.abspath(self.getProjectPath() + "/" + v)) # ["from"], "to"

    def autopopCompiles(self):
        """Automatically adds "compile" actions to the build graph for every
           .C or .CPP file located in the root folder with the build graph.
        """
        bgPath, _ = os.path.split(self.buildGraphPath)
        srcPath = os.path.abspath(bgPath)
        for filename in os.listdir(srcPath):
            if filename.endswith(".c") or filename.endswith(".cpp"):
                fileRoot, _ = os.path.splitext(filename)
                self.edges.append({
                    "from": "%s" % filename,
                    "action": "compile",
                    "to": "obj/%s.obj" % fileRoot
                })

    def getProjectName(self):
        """Extracts project name from the folder where the build graph is
           stored.
        """
        projPath, _ = os.path.split(self.buildGraphPath)
        _, projName = os.path.split(projPath)
        return projName

    def autopopArchives(self):
        """Automatically adds an "archive" actions to the build graph that
           collects all .obj files NOT beginning with "main" or "test" into a
           static library. Unlike the autopopCompiles() method, this is based
           on existing vertices in the build graph, not folder contents. The
           static library will be named after the project.
        """
        vertices = self.getVertices()
        archPath = "lib/%s.lib" % self.getProjectName()
        for v in vertices:
            # v is a string that may contain path information
            _, filename = os.path.split(v)
            if filename.startswith("main") or filename.startswith("test"):
                continue
            if filename.endswith(".obj"):
                self.edges.append({
                    "from": v,
                    "action": "archive",
                    "to": archPath
                })

    def autopopLinks(self):
        """Automatically adds a "link" operation for each "main" or "test"
           vertex. By default, this will link to an executable in the "bin/"
           folder. All such operations are also linked against a static library
           assumed to be generated from project source objects in the "archive"
           stage (see autopopArchives() for details.) The following factors are
           considered when naming the output:
           * "test" or "test_" will generate executables with identical names
           * "main" will generate an executable with the project name
           * "main_" will generate an executable with the trailing name. For
             example, "main_computeStuff.obj" will generate a
             "computeStuff.exe" executable.
        """
        vertices = self.getVertices()
        archPath = "lib/%s.lib" % self.getProjectName()
        for v in vertices:
            _, filename = os.path.split(v)
            if filename.endswith(".obj"):
                if filename.startswith("main") or filename.startswith("test"):
                    fileRoot, _ = os.path.splitext(filename)
                    if filename.startswith("main_"):
                        fileRoot = filename.split("_", 1)[1]
                    if filename.startswith("main"):
                        fileRoot = self.getProjectName()
                    binPath = "bin/%s.exe" % fileRoot
                    self.edges.append({
                        "from": archPath,
                        "action": "link",
                        "to": binPath
                    })
                    self.edges.append({
                        "from": v,
                        "action": "link",
                        "to": binPath
                    })

def build(root):
    """Initializes a recursive traversal of the build graph, walking backwards
       from each final vertex.
    """
    bg = BuildGraph(root)
    finals = bg.getFinalVertices()
    for v in finals:
        bg.traverse(v)

def clean(root):
    """Deletes all intermediate build products from the package folder.
    """
    bg = BuildGraph(root)
    vi = bg.getIntermediateVertices()
    allFolders = []
    for v in vi:
        fullPath = bg.getProjectPath() + "/%s" % v
        fullFolder, _ = os.path.split(fullPath)
        allFolders.append(fullFolder)
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    vf = bg.getFinalVertices()
    for v in vf:
        fullPath = bg.getProjectPath() + "/%s" % v
        fullFolder, _ = os.path.split(fullPath)
        allFolders.append(fullFolder)
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    # finally, check set of product folders to see if it is safe to remove them
    productFolders = set(allFolders)
    for productFolder in productFolders:
        contents = os.listdir(productFolder)
        if len(contents) == 0:
            os.rmdir(os.path.abspath(productFolder))

def init(root):
    """Creates a new build_graph.csv table in the given folder. (An error is
       thrown if one already exists.) Auto-populates actions using the
       "auto-pop" algorithms defined in corresponds BuildGraph methods.
    """
    bg = BuildGraph(root)
    bg.autopopCompiles()
    bg.autopopArchives()
    bg.autopopLinks()
    bg.save()

def help():
    """
    """
    with open(EPIC_PATH + "/README.rst", 'r') as f:
        print(f.read())

def main(action="help", root=os.getcwd()):
    """Performs a specific action against a package root. A list of optional
       action-specific arguments can also be provided.
    """
    root = os.path.abspath(root + "/build_graph.csv")
    if action == "build":
        build(root)
    elif action == "clean":
        clean(root)
    elif action == "init":
        init(root)
    elif action == "help":
        help()
    else:
        raise Exception("Unsupported action '%s'" % action)

if __name__ == "__main__":
    main(*sys.argv[1:])
