"""
"""

import os
import datetime

def build(package):
    """Builds singular *include* header in current directory (maybe should
        be in inc/?). Aggregates all .h files in root-level folder, assuming
        each one has its own #ifndef checks where appropriate.
    """
    headerName = package._getName() + ".h"
    now = datetime.datetime.utcnow()
    lines = []
    lines.append("/* Automatic package header from epic")
    lines.append("   Generated " + now.strftime("%Y/%m/%d %H:%M:%S"))
    lines.append("*/")
    lines.append("")
    for header in package._getFilteredContents(r"\.h$"):
        if header == headerName:
            continue
        lines.append('#include "%s"' % header)
    lines.append("")
    headerPath = package.absDir + os.path.sep + headerName
    if False and os.path.isfile(headerPath):
        raise Exception("A header with the package name already exists")
    with open(headerPath, "w") as f:
        f.write("\n".join(lines))
    return headerPath

