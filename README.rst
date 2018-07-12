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
