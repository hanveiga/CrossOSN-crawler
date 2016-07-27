import urllib2
import json
import re
import sys

def crawl_photo(url):
    print 'This serves as an example of what one can get from our dataset.\
           Please go through Instagram official API for extensive use.'

    response = urllib2.urlopen(url)
    text = response.read()
    scripts = re.findall("<script.*?>(.*?)</script>",text)
    block = scripts[4]
    json_photo = json.loads(block[21:-1])
    return json_photo

if __name__=='__main__':
    print crawl_photo(sys.argv[1])
