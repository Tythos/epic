"""Runners are stateless functions that transform project/package source (or
   intermediate artifacts) into a set of destination files. These are
   effectively build actions.
"""

from epic.runners import docs, exes, header, lib, tests
