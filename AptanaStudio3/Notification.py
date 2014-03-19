#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
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
        "title": {
            "required": True,
            "description": "Title of the Notification"
        },
        "subtitle": {
            "required": False,
            "description": "Subtitle of the Notification"
        },
        "message": {
            "required": True,
            "description": "Body text for the notification."
        },
    }
    output_variables = {
    }
    
    __doc__ = description
    
    
    def main(self):
        title = self.env.get('title')
        subtitle = self.env.get('subtitle', "")
        message = self.env.get('message')
        
        open_url = self.env.get('open_url')
        
        # should probably check if user is logged in and skip if not
        
        notify(title, subtitle, message)

        
        self.output("Posted Notification %s" % title)
    

if __name__ == '__main__':
    processor = Notification()
    processor.execute_shell()
    

