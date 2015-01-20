#!/usr/bin/env python

import re
import urllib2
from urlparse import urlparse
from autopkglib import Processor, ProcessorError

__all__ = ["Python3URLProvider"]

BASE_URL = 'https://www.python.org/'
INDEX_PAGE = 'downloads/'
re_url = '(?P<url>https://.*/python-(?P<version>3\.\d+\.\d+).*\.pkg)'

class Python3URLProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
			"base_url": {
				"required": False,
				"description": "Default is '%s." % BASE_URL,
			},
			"download_page": {
				"required": False,
				"description":
						"page to find download on, default  is '%s." % INDEX_PAGE,
			},
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

        def get_url(self, base_url, download_page, re_url):
                index_url = "/".join((base_url, download_page))
                try:
                        f = urllib2.urlopen(index_url)
                        content = f.read()
                        f.close()
                except BaseException as e:
                        raise ProcessorError('Could not retrieve URL: %s' % index_url)

                re_pattern = re.compile(r'%s' % re_url)

                m = re_pattern.search(content)
                if not m:
                    raise ProcessorError(
                    "Couldn't find download URL in %s"
                    % (index_url))

                return { 'url': m.group("url"), 'version': m.group("version") }

        def main(self):
            result = self.get_url(BASE_URL, INDEX_PAGE, re_url)
            self.env['url'] = result['url']
            self.env['version'] = result['version']
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = Python3URLProvider()
        processor.execute_shell()