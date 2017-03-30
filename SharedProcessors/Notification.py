#!/usr/bin/env python
#
# Copyright 2014-2017 Armin Briegel
#

from autopkglib import Processor, ProcessorError

from Foundation import NSUserNotification, NSUserNotificationCenter


__all__ = ["Notification"]

# from here: https://gist.github.com/pudquick/8513781

# Banner-style (default)

def notify(title, subtitle, text):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    notification.setSubtitle_(str(subtitle))
    notification.setInformativeText_(str(text))
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)



class Notification(Processor):
    description = "Uses OS X Notification Center to provide info to the user."
    input_variables = {
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):        
        title = self.env['NAME']

        message = ""
        pkg_summary = self.env.get('pkg_creator_summary_result')
        download_summary = self.env.get('url_downloader_summary_result')
        if pkg_summary is not None:
            
            message = "New package!"

        elif download_summary is not None:
            message = "New download!"

        if message is not "":   
            version = self.env.get('version')
            if version is not None:
                message = message + (" Version: %s" % version)

            # should probably check if user is logged in and skip if not
            notify(title, "", message)
            self.output("Posted Notification %s" % title)


if __name__ == '__main__':
    processor = Notification()
    processor.execute_shell()
    

