EPIC
====

Extraordinary Packages in C/C++
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EPIC is a useful tool for organizing both the build processes and dependencies for
your cross-platform C/C++ packages. It works with multiple build tools, using
familiar paradigms and a transparent, customizable build graph.

Initialize
----------

Once you've installed EPIC (making sure the folder is in your PATH and PYTHONPATH
enviornmental variables), browse to a folder that contains some C/C++ code you'd
like to create a package for. Then, type the following command:

 > epic init

This will automatically create two files:

#. A "build_graph.csv" table, which defines edges of the build graph for various
   operations (compiling .CPP source, archiving non-main objects, linking main
   objects). Additional operations will be implemented in the future, but this
   build graph can be customized for your particular project needs once created.

#. A "epic_package.json" file, which contains default package values for a UNI
   (universal namespace identifier), SemVer (semantic versioning numbers), and
   dependencies (an empty Array).

Building
--------

Once you've inspected (and customized, if necessary) the build graph defined in
*build_graph.csv*, you can run the following command from your package folder:

 > epic build

This will back out each operation from the build graph, performing them when it
detects changes have been made (or when the build artifact has not yet been
generated). Right now, operations are mapped to MSVC (Microsoft Visual Studio)
command-line invocations, but these are set up to be customizable. Future releases
will also support the LLVM/Clang and GCC toolchains.

In the default build graph, final artifacts will include:

* .EXE programs for all "main_*.cpp" source files

* .LIB static libraries that archive all non-main ".cpp" source files

Future releases may also support dynamic library generation, but of course this
will be a little bit more involved because of the platform-specific considerations.

Cleaning
--------

From the command line, you can clean up all intermediate build products by running
the following comamnd from your package folder:

 > epic clean

You can also include an optional "--all" flag; in that case, all final build
products (.EXE and .LIB files) will be removed, as well.

Future Features
---------------

The immediate, and most daunting, task is to determine how dependencies are
identified, resolved, and built against. There are some initial thoughts in the
*dep notes.txt* file. These will primarily leverage the contents of the
*epic_package.json* file and an environmental variable (*EPIC_REPO*) that
identifies the path in which EPIC package folders are stored on a particular
system.

