import os
import json
import requests
import re
import csv

from urlparse import urlparse

'''
This script validates and tests the Status Codes for URLs in the
org-id register. It creates `url_testing.csv` which contains
the results of the validation and tests for each url.

Remember to `git pull` `git merge master` before running
`python url_tester.py` so that the most up to date register
is being used!
'''

def url_status(url):
    '''
    attempts to connect to valid url. Returns status status_code
    if successful, 'error connecting' if not. Returns 'not valid'
    if not a valid url
    '''
    if uri_validator(url) == True:
        try:
            r = requests.head(url, timeout=10)
            print(url, r.status_code)
            return url, r.status_code
        except requests.ConnectionError:
            print('Failed to connect to ', url)
            return url, 'error connecting'
        except requests.Timeout as e:
            print(str(e))
            return url, 'Timeout Error'
    else:
        print(url, 'not valid')
        return url, 'not valid'

def uri_validator(url):
    '''
    tests that url is valid. if it isn't, returns
    False, and we can note this in the output
    '''
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False

def main():
    with open('url_testing.csv', 'w') as outputfile:
        csvwriter  = csv.writer(outputfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['List', 'Field', 'URL', 'Status'])

        '''
        walk through all of the registration agency lists to test url_status
        '''
        for subdir, dirs, files in os.walk('lists'):
            for reglistfile in files:
                p = re.compile(".*.json")
                nourls = False
                if p.match(reglistfile):
                    filepath = os.path.join(subdir, reglistfile)
                    reglist = json.load(open(filepath))
                    print(reglist['code'])
                    '''
                    urls can be found in two fields in the list schema:
                        "url", which should always exist
                        "access.publicDatabase", which may be used if there
                           is an downloadable dataset
                    urls can also often be found in "description" and
                    "access.onlineAccessDetails", but we don't test them here
                    '''
                    if reglist['url'] and reglist['access']['publicDatabase']:
                        urls = {'list_url': reglist['url'], 'database_url': reglist['access']['publicDatabase']}
                        url, status = url_status(urls['list_url'])
                        csvwriter.writerow([reglist['code'], 'url', url, status])
                        url, status = url_status(urls['database_url'])
                        csvwriter.writerow([reglist['code'], 'access.publicDatabase', url, status])
                    elif reglist['url']:
                        urls = {'list_url': reglist['url']}
                        url, status = url_status(urls['list_url'])
                        csvwriter.writerow([reglist['code'], 'url', url, status])
                    else:
                        csvwriter.writerow([reglist['code'], 'url', 'NO URL', 'NO URL'])

if __name__ == '__main__':
    main()
