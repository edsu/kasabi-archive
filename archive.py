#!/usr/bin/env python

"""
uploads Kasabi datasets downloaded to a dataset directory to Internet Archive 
before you can run this you will need to run fetch.py and then create a 
~/.boto that looks like

[Credentials]
ia_access_key_id=[your-internet-archive-access-key]
ia_secret_access_key=[your-internet-archive-secret-access-key]

If you need keys visit: http://archive.org/account/s3.php
"""

import os
import sys
import boto

from boto.s3.key import Key

ia = boto.connect_ia()
bucket = ia.create_bucket('kasabi')

for filename in os.listdir('dataset'):
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename("dataset/%s" % filename)
    print "saved %s to internet archive as %s" % (filename, k.key)
