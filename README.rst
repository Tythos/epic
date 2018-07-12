Excellent Packages In C++
=========================

EPIC is a bare-bones cross-platform C++ package building tool. It assumes a
targeted package folder has a flat collection of .H and .CPP files, in which
tests begin with "test_" and entry points begin with "main_".

Building
--------

The "epic build" command will:
 * Compile all .CPP into object files
 * Archive all non-test, non-main object files into a static library
 * Link all test and main object files against that static library to produce
   binary executables

Cleaning
--------

The "epic clean" command will delete all contents of the following folders:
 * bin
 * lib
 * obj

Configuration
-------------

Customized build options can be specified within a *package.json* file. At the
moment, this include support for pre-processing "#DEFINE [key]=[value]" macros
in a "define" object. Future options may include traditional package attribution
(author, etc) and conditional parameters for specific builds (architectures,
configurations).

Metadata uniquely identifying the package is *not* included in the package.json
file; instead:
 * The UNI is specified by the second-topmost folder name
 * The semantic version is specified by the topmost folder name
 * Source repository information is specified by the Git config data

Other fields included in package.json include:
 * *dependencies*, an object listing UNI and semver constriants for each package
   dependency as key-value pairs
 * *summary*, a single-sentance

Additional package information can include, at the top level of the package:
 * A *.gitignore* file
 * A *README.rst* file (outlining the package purpose and contents; specific
   documentation should be integrated into source files for extraction and
   publishing by a tool like Doxygen)
 * A *LICENSE* file

Folders
-------

EPIC packages must be contained in folders with the following sequence:
 * Top-level folder name must be the semantic version of the package
 * Second-to-top-level folder name must be the UNI of the package

For example, a package with the UNI "edu.hmc.eng.utils" and semantic version
1.2.3 must be located in "edu.hmc.eng.utils/1.2.3".

EPIC assumes all source and header files are stored at the top level of the
package (adjacent to *package.json*, etc.). This makes it easy to start
building an existing batch of source code as a package. However, source files
and headers within subfolders can still be referenced from #include directives;
they will simply not be directly compiled or integrated into the static
library when the *build* action is invoked.
