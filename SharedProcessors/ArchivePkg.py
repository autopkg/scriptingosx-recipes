#!/usr/bin/env python
#
# Copyright 2017 Armin Briegel
#

from autopkglib import Processor, ProcessorError

import shutil
import os


class ArchivePkg(Processor):
    description = "Copies a Pkg to a given folder."

    input_variables = {
        "pkg_path": {
            "required": True,
            "description": "Path to the pkg to archive."
        },
        "archive_path": {
             "required": True,
             "description": "Path to the archive folder."
        },
    }

    output_variables = {
        "archived_pkg_path": {
             "description": "Path to the archived pkg."
        },
        "archived_pkg_summary_result": {
            "description": "Description of interesting results."
        },
    }

    __doc__ = description

    def main(self):
        archive_path = self.env["archive_path"]
        pkg_path = self.env["pkg_path"]

        pkg_filename = os.path.basename(pkg_path)
        archived_pkg_path = os.path.join(archive_path, pkg_filename)

        if not os.path.isdir(archive_path):
            raise ProcessorError("Archive %s does not exist!" % archive_path)

        if not os.path.exists(pkg_path):
            raise ProcessorError("Pkg %s does not exist!" % pkg_path)

        if os.path.exists(archived_pkg_path) and os.path.getmtime(archived_pkg_path) >= os.path.getmtime(pkg_path):
            self.output("%s already exists in %s and is not older. Not copying." % (pkg_filename, archive_path))
        else:
            shutil.copy2(pkg_path, archive_path)
            self.output("Archived %s in %s" % (pkg_path, archive_path))
            self.env["archived_pkg_summary_result"] = {
                'summary_text': 'The following packages were archived:',
                'data': {'archived_pkg_path': archived_pkg_path}
            }
            self.env["archived_pkg_path"] = archived_pkg_path


if __name__ == '__main__':
    processor = ArchivePkg()
    processor.execute_shell()
