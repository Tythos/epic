"""A Porter defines a basic interface for importing/exporting an Epic
   configuration to/from an IDE project format. Unlike Builders, this
   is a stateless interface that either 1) generates an epic configuration
   (package.json) from an IDE project, or 2) generates an IDE project from an
   epic configuration. Source files always reference those at the base of the
   project, but a seperate subdirectory will be created (in the case of 2))
   with all related IDE project files.
"""

class Porter(object):
    """
    """

    @classmethod
    def export(self):
        """
        """
        pass

    @classmethod
    def import(self):
        """
        """
        pass
