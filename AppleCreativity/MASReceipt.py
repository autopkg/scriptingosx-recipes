#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
#

import os

from autopkglib import Processor, ProcessorError

class MASReceipt(Processor):
    description = "Will either delete the _MASReceipt folder or replace it with a dummy receipt."
    
    input_variables = {
        "mas_action": {
            "required": True,
            "description": "Set to 'delete' to remove the _MASReceipt folder or to 'dummy' to replace with dummy receipt. Any other value will do nothing."
        },
        "app_path": {
            "required": True,
            "description": "path to the .app bundle to act on"
        },
        "dummy_receipt_content": {
            "required": False,
            "description": "Text content written into the dummy receipt file. Default is 'dummy receipt' but you can change this if you want to leave messages."
        },
    }
    
    output_variables = {
    }
    
    __doc__ = description
    
    def main(self):
        app_path =os.path.expanduser(self.env["app_path"])
        mas_action = self.env["mas_action"]
        dummy_receipt_content = self.env.get("dummy_receipt_content", "dummy receipt")
        
        if os.path.basename(app_path).endswith('.app'):
            masreceipt_dir_path = os.path.join(app_path, "Contents", "_MASReceipt")
        elif os.path.basename(app_path) == "_MASReceipt":
            masreceipt_dir_path = app_path
        else:
            raise ProcessorError("Not an app or MASReceipt folder: %s" % (pathname))
        
        masreceipt_file_path = os.path.join(masreceipt_dir_path, "receipt")
        
        if mas_action in ("dummy", "delete"):
            if os.path.exists(masreceipt_dir_path):
                if os.path.exists(masreceipt_file_path):
                    os.remove(masreceipt_file_path)
            
            if mas_action == "dummy":
                self.output('Replacing %s with dummy.' % (masreceipt_file_path))
                try:
                    f = open(masreceipt_file_path, 'w')
                    f.write(dummy_receipt_content + "\n")
                finally:
                    f.close()
            elif mas_action == "delete":
                if os.path.exists(masreceipt_dir_path):
	                self.output('Deleting %s' % (masreceipt_dir_path))
	                os.rmdir(masreceipt_dir_path)
        

if __name__ == '__main__':
    processor = MASReceipt()
    processor.execute_shell()
    
