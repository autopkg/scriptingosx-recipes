#!/usr/bin/env python
#
# Copyright 2014 Armin Briegel
#

import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["AptanaStudio3URLProvider"]


APTANASTUDIO3_BASE_URL = "http://aptana.com/products/studio3/download"
APTANASTUDIO3_DMG_RE = r'(?P<url>download\.aptana\.com\/studio3\/standalone\/.*/mac\/Aptana_Studio_3_Setup_.*\.dmg)'


class AptanaStudio3URLProvider(Processor):
    description = "Provides URL to the latest release of AptanaStudio3."
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is '%s'." % APTANASTUDIO3_BASE_URL,
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest release of AptanaStudio3.",
        },
    }
    
    __doc__ = description
    
    def get_aptanastudio3_dmg_url(self, base_url):
        re_aptanastudio3_dmg = re.compile(APTANASTUDIO3_DMG_RE)
        # Read HTML index.
        try:
            f = urllib2.urlopen(base_url)
            html = f.read()
            f.close()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (base_url, e))
        #self.output(html)
        
        # Search for download link.
        m = re_aptanastudio3_dmg.search(html)
        self.output(m)
        if not m:
            raise ProcessorError("Couldn't find AptanaStudio3 download URL in %s" % base_url)
        
        # Return URL
        url = "http://" + m.group("url")
        return url
    
    def main(self):
        # Determine base_url.
        base_url = self.env.get('base_url', APTANASTUDIO3_BASE_URL)
        
        self.env["url"] = self.get_aptanastudio3_dmg_url(base_url)
        self.output("Found URL %s" % self.env["url"])
    

if __name__ == '__main__':
    processor = AptanaStudio3URLProvider()
    processor.execute_shell()
    

