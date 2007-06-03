import os
import re

import django.test.simple
from django.test import TestCase
from ietf.urls import urlpatterns
import ietf.settings
import ietf.tests

def run_tests(module_list, verbosity=1, extra_tests=[]):
    module_list.append(ietf.tests)
    return django.test.simple.run_tests(module_list, verbosity, extra_tests)

class UrlTestCase(TestCase):
    def setUp(self):
        from django.test.client import Client
        self.client = Client()

        # find test urls
        self.testurls = []
        for root, dirs, files in os.walk(ietf.settings.BASE_DIR):
            if "testurl.list" in files:
                filename = root+"/testurl.list" # yes, this is non-portable
                file = open(filename) 
                for line in file:
                    urlspec = line.split()
                    if len(urlspec) == 2:
                        code, testurl = urlspec
                        goodurl = None
                    elif len(urlspec) == 3:
                        code, testurl, goodurl = urlspec
                    else:
                        raise ValueError("Expected 'HTTP_CODE TESTURL [GOODURL]' in %s line, found '%s'." % (filename, line))
                    self.testurls += [ (code, testurl, goodurl) ]

    def testCoverage(self):
        covered = []
        patterns = [pattern.regex.pattern for pattern in urlpatterns]
        for code, testurl, goodurl in self.testurls:
            for pattern in patterns:
                if re.match(pattern, testurl):
                    self.covered.append(pattern)
        # We should have at least one test case for each url pattern declared
        # in our Django application:
        self.assertEqual(set(patterns), set(covered), "Not all the application URLs has test cases.")

    def testUrls(self):
        for code, testurl, goodurl in self.testurls:
            response = self.client.get(testurl)
            print "%s %s" % (response.status_code, testurl)
            self.assertEqual(response.status_code, code, "Unexpected response code from URL '%s'" % (testurl))
            # TODO: Add comparison with goodurl
