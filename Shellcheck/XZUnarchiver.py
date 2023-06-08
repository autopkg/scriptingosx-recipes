#!/usr/local/autopkg/python
#
# Copyright 2019 Armin Briegel
# based on LZMADecompress by Nick McSpadden 2013
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#I would just like to state, for the record, I am fully aware of how awful this script is.
#I will eventually fix it to make it much more robust, but it's more of a "get-it-done" kind of solution.

import subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["XZUnarchiver"]

class XZUnarchiver(Processor):
	description = "Decompresses an xz file using xz, a precompiled binary for macOS"
	input_variables = {
		"archive_path": {
			"required": True,
			"description": ("Path to .xz file."),
		},
		"decompressor": {
			"required": True,
			"description": ("Path to xz binary."),
		}
	}
	output_variables = {
		"decompressed_path": "The unarchived result.",
	}

	__doc__ = description

	def decompress_the_file(self):
		file = self.env.get("archive_path")
		if not file:
			raise ProcessorError("archive_path not found: %s" % (file))
		xz = self.env.get("decompressor")
		if not xz:
			raise ProcessorError("xz binary not found: %s" % (xz))
		cmd = [xz,'-k', '-f', '--decompress',file]
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(output, errors) = proc.communicate()
		return errors      

	def main(self):
		'''Does nothing except decompresses the file'''
		if "archive_path" in self.env:
			self.output("Using input XZ file %s decompressing with %s" % (self.env["archive_path"], self.env["decompressor"]))
		self.decompress_the_file()
		self.env["decompressed_path"] = self.env["archive_path"][:-3]
		self.output("Decompressed: %s" % self.env["decompressed_path"])


if __name__ == '__main__':
    processor = XZUnarchiver()
    processor.execute_shell()
    

