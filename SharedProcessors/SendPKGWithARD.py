#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
#

from autopkglib import Processor, ProcessorError

from Foundation import *

def executeAppleScript(source):
    appleScript = NSAppleScript.alloc().initWithSource_(source)
    return appleScript.executeAndReturnError_(objc.NULL)


class SendPKGWithARD(Processor):
    description = "Takes a pkg and sends it to a given list of computers with ARD."
    
    input_variables = {
        "pkg_path": {
            "required": True,
            "description": "Path to the pkg."
        },
        "computer": {
            "required": False,
            "description": "Name of a single computer in ARD. One of computer or computer_list must be set."
        },
        "computer_list": {
            "required": False,
            "description": "Name of a computer_list in ARD. One of computer or computer_list must be set."
        },
    }
    
    output_variables = {
    }
    
    __doc__ = description

    
    def main(self):
        pkg_path = self.env["pkg_path"]
        
        computer_name = self.env.get("computer", None)
        computer_list = self.env.get("computer_list", None)
        
        if computer_list != None:
            target = "computer list \"%s\"" % (computer_list)
        elif computer_name != None:
            target = "computer \"%s\"" % (computer_name)
        else:
            raise ProcessorError("One of the input variables 'computer' or 'computer_list' must be set!")

        script_source = """set thepkg to (POSIX file "%s") as alias
                tell application "Remote Desktop"
    	            set t to make new install package task with properties {delegating to task server:false, encrypting:true, packages:{thepkg}, stopping on error:false}
    	            execute t on %s
                end tell
                """
        
        scriptresult = executeAppleScript( (script_source % (pkg_path, target)) )

        self.output("Script Result: ")
        self.output(scriptresult)
        



if __name__ == '__main__':
    processor = SendPKGWithARD()
    processor.execute_shell()
    

