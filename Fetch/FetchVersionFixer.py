#!/usr/bin/python
#
# Copyright 2013 The Pennsylvania State University.
#
# Created by Matt Hansen (mah60@psu.edu) on 2013-11-12.
# Based on AutoPkg VersionFixers by Per Olofsson (per.olofsson@gu.se)
#
# As of version Fetch 5.7.3 the Contents/Info.plist CFBundleVersion key 
# contains a Unicode Zero-width space that causes us lots of problems.

import re

from autopkglib import Processor, ProcessorError


__all__ = ["FetchVersionFixer"]


class FetchVersionFixer(Processor):
    description = "Removes unicode characters from Fetch version."
    input_variables = {
        "version": {
            "required": True,
            "description": "Dirty Fetch version string.",
        },
    }
    output_variables = {
        "version": {
            "description": "Clean Fetch version string.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        
        self.env["version"] = self.env.get('version').encode("ascii", "ignore")
        self.output("Cleaned version string %s" % self.env["version"])

if __name__ == '__main__':
    processor = FetchVersionFixer()
    processor.execute_shell()
