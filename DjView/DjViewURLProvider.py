#!/usr/bin/env python

import re
import urllib, urllib2
from urlparse import urlparse
from autopkglib import Processor, ProcessorError

__all__ = ["DjViewURLProvider"]

search_url = 'http://sourceforge.net/projects/djvu/rss?path=/DjVuLibre_MacOS'
re_pattern = '(?P<url>http://sourceforge\.net/projects/djvu/files/DjVuLibre_MacOS/(?P<version>.*?)/DjVuLibre-.*?.dmg)'
#re_url = '(?P<url>https://.*/python-(?P<version>3\.\d+\.\d+).*\.pkg)'

class DjViewURLProvider(Processor):
        '''Provides URL to the latest version of the DjView for Mac project. http://sourceforge.net/projects/djvu/'''

        input_variables = {
			"url": {
				"required": False,
				"description": "Default is '%s." % search_url,
			},
			"re_pattern": {
				"required": True,
				"description": "Regular expression (Python) to match against page."
			}
        }
        output_variables = {
                'url': {
                        'description': 'First matched sub-pattern from input found on the fetched page'
                },
                'version': {
                		'description': 'version of the package extracted from the url'
                },
        }

        description = __doc__

        def get_url(self, url, re_pattern):
                try:
                        f = urllib2.urlopen(url)
                        content = f.read()
                        f.close()
                except BaseException as e:
                        raise ProcessorError('Could not retrieve URL: %s' % index_url)

                re_pattern = re.compile(r'%s' % re_pattern)

                m = re_pattern.search(content)
                if not m:
                    raise ProcessorError(
                    "Couldn't find download URL in %s"
                    % (index_url))

                return { 'url': m.group("url"), 'version': m.group("version") }

        def main(self):
            url = self.env.get('url', search_url)
            pattern = self.env.get('re_pattern', re_pattern)
            result = self.get_url(url, pattern)
            self.env['url'] = result['url']
            
            #the version gained from the url has a weird format liek 3.5.27%2B4.10, we are only interested in the second part
            v = urllib.unquote(result['version'])
            v = v.rsplit('+', 1)[1]
            self.env['version'] = v
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = DjViewURLProvider()
        processor.execute_shell()