#!/usr/bin/env python
#
# Copyright 2014-2017 Armin Briegel
#

from __future__ import absolute_import
from autopkglib import Processor, ProcessorError

from Foundation import NSUserNotification, NSUserNotificationCenter
from AppKit import NSWorkspace, NSImage

import os

__all__ = ["Notification"]

# from here: https://gist.github.com/pudquick/8513781

# Banner-style (default)

def notify(title, subtitle, text, fileType = None):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    notification.setSubtitle_(str(subtitle))
    notification.setInformativeText_(str(text))
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
    if fileType is not None:
        file_icon = NSWorkspace.sharedWorkspace().iconForFileType_(fileType)
        notification.setContentImage_(file_icon)
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


class Notification(Processor):
    description = "Uses OS X Notification Center to provide info to the user."
    input_variables = {
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):        
        title = self.env.get('NAME')

        message = ""
        result_path = None
        fileType = None

        archive_summary = self.env.get('archive_summary_result')
        pkg_summary = self.env.get('pkg_creator_summary_result')
        download_summary = self.env.get('url_downloader_summary_result')

        if archive_summary is not None:
            message = "Archived new file!"
            result_path = self.env.get('archived_file_path')
        elif pkg_summary is not None:
            message = "New package!"
            result_path = self.env.get('pkg_path')
        elif download_summary is not None:
            message = "New download!"
            result_path = self.env.get('pathname')

        if result_path is not None:
            (filename, file_type) = os.path.splitext(result_path)

        if message is not "":   
            version = self.env.get('version')
            if version is not None:
                message = message + (" Version: %s" % version)

            # should probably check if user is logged in and skip if not
            notify(title, "", message, file_type)
            self.output("Posted Notification %s" % title)


if __name__ == '__main__':
    processor = Notification()
    processor.execute_shell()
    

