#!/usr/bin/env python
#
# Copyright 2017 Armin Briegel
#

from __future__ import absolute_import

import os
import shutil

from autopkglib import Processor, ProcessorError


class Archive(Processor):
    description = "Copies (archives) a Pkg or Dmg to a given folder."

    input_variables = {
        "pkg_path": {
            "required": False,
            "description": "Path to the pkg to archive. If no pkg_path is given, will try pathname instead."
        },
        "pathname": {
            "required": False,
            "description": "path to the download (dmg or zip) to archive. Will not be used if pkg_path is set."
        },
        "archive_directory": {
             "required": True,
             "description": "Path to the archive folder."
        },
        "archive_subdir": {
             "required": False,
             "description": "subdir in the archive folder"
        },
    }

    output_variables = {
        "archived_file_path": {
             "description": "Path to the archived file."
        },
        "archive_summary_result": {
            "description": "Description of interesting results."
        },
    }

    __doc__ = description

    def main(self):
        archive_path = self.env.get("archive_directory")
        archive_path = os.path.expanduser(archive_path)

        file_path = self.env.get("pkg_path")

        if file_path is None:
            file_path = self.env.get("pathname")

        if file_path is None:
            self.output("neither pkg_path nor pathname are set, not archiving")
        else:
            if not os.path.isdir(archive_path):
                raise ProcessorError("Archive %s does not exist!" % archive_path)
            
            subdir = self.env.get("archive_subdir")
            if subdir is not None:
                archive_path = os.path.join(archive_path, subdir)
                if not os.path.exists(archive_path):
                    os.makedirs(archive_path)

            file_name = os.path.basename(file_path)
            archived_file_path = os.path.join(archive_path, file_name)

            if not os.path.exists(file_path):
                raise ProcessorError("File %s does not exist!" % file_path)

            if os.path.exists(archived_file_path) and os.path.getmtime(archived_file_path) >= os.path.getmtime(file_path):
                self.output("%s already exists in %s and is not older. Not copying." % (file_name, archive_path))
            else:
                shutil.copy2(file_path, archive_path)
                self.output("Archived %s in %s" % (file_path, archive_path))
                self.env["archive_summary_result"] = {
                    'summary_text': 'The following files were archived:',
                    'data': {"archived_file_path": archived_file_path}
                }
                self.env["archived_file_path"] = archived_file_path


if __name__ == '__main__':
    processor = Archive()
    processor.execute_shell()
