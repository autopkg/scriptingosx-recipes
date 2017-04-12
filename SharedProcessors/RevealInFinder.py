#!/usr/bin/env python
#
# Copyright 2014-2017 Armin Briegel
#

from autopkglib import Processor, ProcessorError

from Foundation import *

import os.path

def executeAppleScript(source):
    appleScript = NSAppleScript.alloc().initWithSource_(source)
    return appleScript.executeAndReturnError_(objc.NULL)


class RevealInFinder(Processor):
    description = "Reveals a given path in the Finder."
    
    input_variables = {
    }
    
    output_variables = {
    }
    
    __doc__ = description

    
    def main(self):        
        reveal_path = None
        archive_summary = self.env.get('archive_summary_result')
        pkg_summary = self.env.get('pkg_creator_summary_result')
        download_summary = self.env.get('url_downloader_summary_result')
        if archive_summary is not None:
            reveal_path = self.env.get('archived_file_path')
        elif pkg_summary is not None:
            reveal_path = self.env.get('pkg_path')
        elif download_summary is not None:
            reveal_path = self.env.get('pathname')

        if reveal_path is not None:   
            # should probably check if user is logged in and skip if not
            script_source = """tell app "Finder" to reveal posix file "%s" """
        
            scriptresult = executeAppleScript(script_source % reveal_path)      



if __name__ == '__main__':
    processor = RevealInFinder()
    processor.execute_shell()
