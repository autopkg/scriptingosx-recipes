#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
#

from autopkglib import Processor, ProcessorError

from Foundation import *

def executeAppleScript(source):
    appleScript = NSAppleScript.alloc().initWithSource_(source)
    return appleScript.executeAndReturnError_(objc.NULL)


class RevealInFinder(Processor):
    description = "Reveals a given path in the Finder."
    
    input_variables = {
        "reveal_path": {
            "required": True,
            "description": "Path to show in Finder."
        },
    }
    
    output_variables = {
    }
    
    __doc__ = description

    
    def main(self):
        reveal_path = self.env["reveal_path"]
        
        #should check wether file exists here
        
        script_source = """tell app "Finder" to reveal posix file "%s" """
        
        scriptresult = executeAppleScript( (script_source % (reveal_path)) )

        self.output("Script Result: ")
        self.output(scriptresult)
        



if __name__ == '__main__':
    processor = RevealInFinder()
    processor.execute_shell()
    

