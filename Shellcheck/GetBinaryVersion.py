#!/usr/bin/env python
#
# Copyright 2019 Armin Briegel

import re
import subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["GetBinaryVersion"]

class GetBinaryVersion(Processor):
    description = "Gets the version of a binary by running `binary --version`"
    input_variables = {
        "binary_path": {
            "required": True,
            "description": ("Path to the binary."),
        },
        "version_argument": {
            "required": False,
            "description": ("argument passed to binary to retrieve the version, `--version` is the default"),
        },
        "re_pattern": {
            "required": False,
            "description": ("RE Pattern used to locate the version string in the output."),
        },
    }
    output_variables = {
        "version": "The version of the binary."
    }

    __doc__ = description

    def getVersion(self):
        binary = self.env.get("binary_path")
        if not binary:
            raise ProcessorError("binary_path not found: %s" % (binary))
        version_argument = self.env.get("version_argument", "--version")
        re_string = self.env.get("re_pattern")
        cmd = [binary, '--version']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, errors) = proc.communicate()
        if re_string:
            re_pattern = re.compile(re_string)
            match = re_pattern.search(output)
            if not match:
                raise ProcessorError("No match found for version string in: %s" % output)
            return match.group(match.lastindex or 0)
        else:
            return output      

    def main(self):
        if "binary_path" in self.env:
            self.output("asking binary %s for version" % (self.env["binary_path"]))
        self.env["version"] = self.getVersion()
        self.output("Binary version: %s" % self.env["version"])


if __name__ == '__main__':
    processor = GetBinaryVersion()
    processor.execute_shell()
    

