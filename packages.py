"""
"""

import os
import json

class Package(object):
    """Models a package based on a specific path. For the most part this is a
        passive model that provides the Builder with a common interface for
        investigating package properties and organizing contents.
    """

    def __init__(self, path):
        """Initializes a package model from a specific path, loading
           *epic.json* at the package root if it exists and defining an empty
           one if it does not.
        """
        self.path = os.path.abspath(path)
        cfg_path = self.path + os.path.sep + 'epic.json'
        if os.path.isfile(cfg_path):
            with open(cfg_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {'dependencies': []}
            with open(cfg_path, 'w') as f:
                json.dump(self.config, f, indent=4)
