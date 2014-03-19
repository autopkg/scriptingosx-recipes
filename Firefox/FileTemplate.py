#!/usr/bin/python
#
# Copyright 2014 University of Southern California.
#
# Created by Armin Briegel (arminb@usc.edu) on 2014-03-13.
# 

from string import Template

from autopkglib import Processor, ProcessorError


__all__ = ["FileTemplate"]


class FileTemplate(Processor):
    description = "Uses Python's string.Template() class to substitute placeholders in a file with autopkg variables. The placeholders use the default '$identifier' or '${identifier}' syntax."
    input_variables = {
        "template_path": {
            "required": True,
            "description": "Path to the template file to apply the substitution on."
        },
        "destination_path": {
            "required": True,
            "description": "Path where the file with the substition files will be written"
        }
    }
    output_variables = {
    }
    
    __doc__ = description
    
    # Note to self: might want to subclass Template to use '%' notification which seems more common in autopkg
    
    def main(self):
        
        template_path = self.env["template_path"]
        destination_path = self.env["destination_path"]
        
        # should use some logic to search through folders to resolve relativ paths
        
        # should verify template_path exists
        
        infile = open(template_path, 'r')
        template_string = infile.read()
        infile.close()
        
        substituted_string = Template(template_string).safe_substitute(self.env)
        
        outfile = open(destination_path, 'w')
        outfile.write(substituted_string)
        outfile.close()
        
        #self.output("Cleaned version string %s" % self.env["version"])

if __name__ == '__main__':
    processor = FileTemplate()
    processor.execute_shell()
