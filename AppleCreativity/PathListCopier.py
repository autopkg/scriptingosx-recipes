#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
#

import os
import errno
import shutil

import FoundationPlist

from autopkglib import Processor, ProcessorError


# this is from here:
# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def makedir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class PathListCopier(Processor):
    description = """Copies a list of local files and folder to pkgroot. It also compares
                a given path (the app) for its version and does not copy if the version in
                the pkgroot is the same as the the local version."""

    input_variables = {
        "pathname": {
            "required": True,
            "description": "Path to where the files from the list are copied to."
        },
        "check_version_path": {
            "required": False,
            "description": """This processor will attempt to determine the vesion at the
                    local path and pathname. If the version at pathname is the same, then 
                    it will not copy. Otherwise the data at pathname will be overwritten. 
                    If this path is not given, the first item from sourcelist will be 
                    used."""
        },
        "plist_version_key": {
            "required": False,
            "description": """Key to use on the Info.plist to read the version. Default 
            is CFBundleShortVersionString."""
        },
        "sourcelist": {
            "required": True,
            "description": "Array of paths that will be copied to pathname."
        }
    }
    
    output_variables = {
        "version": {
            "description": "The version determined by the process."
        },
        "download_changed": {
            "description": """Boolean indicating if files where actually copied. Using 
                this terminology so that Processors down the path treat it the same way
                 as URLDownloader."""
        },
        "pathname": {
        	"description": """pathname the files were copied to"""
        }
    }
    
    __doc__ = description

    def get_version(self, filepath):
        if os.path.exists(filepath):
            #try to determine the version
        
            version_basename = os.path.basename(filepath)
                    
            # is it an app bundle?
            if version_basename.endswith(".app"):
                filepath = os.path.join(filepath, "Contents", "Info.plist")
        else:
            self.output("Cannot determine version. %s does not exist." % (filepath))
            return None
                
        try:
            plist = FoundationPlist.readPlist(filepath)
            version_key = self.env.get("plist_version_key", "CFBundleShortVersionString")
            version = plist.get(version_key, None)
            self.output("Found version %s in file %s" % (version, filepath))
        
        except FoundationPlist.FoundationPlistException, err:
            raise ProcessorError(err) 
    
        return version  


    
    def main(self):
        
        pathname =os.path.expanduser(self.env["pathname"])
        makedir_p(pathname)
        
        check_version_path = self.env.get("check_version_path", self.env["sourcelist"][0])
        
        source_version = self.get_version(check_version_path)
        
        target_version_path = os.path.join(pathname, os.path.relpath(check_version_path, "/"))
        target_version = self.get_version(target_version_path)
        
        self.env["version"] = source_version

        # if version is equal, don't copy, write message, stop
        if target_version == source_version:
            self.output("versions match! Not copying.")
            self.env["download_changed"] = False
        else:
            self.env["download_changed"] = True
            self.env["pathname"] = pathname
            
            # clean out pathname folder
            shutil.rmtree(pathname)
            
            # copy all files from path list
            for source_item in self.env["sourcelist"]:
                #copy all the things
                dest_item = os.path.join(pathname, os.path.relpath(source_item, "/"))
                self.output("Copying: %s" % (source_item))
                
                makedir_p(os.path.dirname(dest_item))
                
                try:
                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, dest_item, symlinks=True)
                    elif not os.path.isdir(dest_item):
                        shutil.copyfile(source_item, dest_item)
                    else:
                        shutil.copy(source_item, dest_item)
                    self.output("Copied %s to %s" % (source_item, dest_item))
                except BaseException, err:
                    raise ProcessorError("Can't copy %s to %s: %s" % (source_item, dest_item, err))



if __name__ == '__main__':
    processor = PathListCopier()
    processor.execute_shell()
    

