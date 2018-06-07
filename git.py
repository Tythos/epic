"""Behaviors for executing specific Git commands via subprocess
"""

import os
import subprocess

class Repo(object):
    """
    """

    def __init__(self, repoPath):
        """
        """
        self.repoPath = os.path.abspath(repoPath)

    def getTags(self):
        """Returns a dictionary of commit hash => tag entries
        """
        proc = subprocess.Popen(["git", "show-ref", "--tags"], cwd=self.repoPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = proc.communicate()
        tagMap = {}
        for line in stdout.decode("ascii", errors="ignore").splitlines():
            commit, reftag = line.split()
            parts = reftag.split("/")
            tagMap[commit] = parts[-1]
        return tagMap

    def getCommit(self, commit):
        """Checks out a specific commit of the repository, as identified by
           the given commit hash.
        """
        proc = subprocess.Popen(["git", "checkout", commit], cwd=self.repoPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, _ = proc.communicate()

    @classmethod
    def clone(cls, url, toPath):
        """
        """
        subprocess.call(["git", "clone", "-c", "http.sslVerify=false", url, toPath])
        return cls(toPath)
