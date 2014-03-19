#!/usr/bin/python
#

import re

from autopkglib import Processor, ProcessorError


__all__ = ["AptanaStudio3VersionReader"]


class AptanaStudio3VersionReader(Processor):
    description = "Finds Aptana."
    input_variables = {
        "file_path": {
            "required": True,
            "description": "Path to the Aptana Studio 3 version.txt file.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version (three digits, e.g. '3.4.2') of the Version number.",
        },
        "build": {
            "description": "Build number",
        },
    }
    
    __doc__ = description
    
    def main(self):
        file_path = self.env["file_path"]
        
        # read version file
        try:
            f = open(file_path)
            version_text = f.read()
            f.close()
        except BaseException as e:
            raise ProcessorError("Can't read " + file_path)

        re_version = re.compile(r'(?<=VERSION )\d+\.\d+\.\d+')
        re_build = re.compile(r'(?<=BUILD ).+')
        self.env["version"] = re_version.search(version_text).group(0)
        self.env["build"] = re_build.search(version_text).group(0)
        self.output("Version string %s" % self.env["version"])
        self.output("Build string %s" % self.env["build"]) 
        
if __name__ == '__main__':
    processor = AptanaStudio3VersionReader()
    processor.execute_shell()
