#!/usr/bin/env python

"""
Downloads the Kasabi dataset snapshots.
"""

import os
import gzip
import requests


class Dataset:
    def __init__(self, name, license, url):
        self.name = name
        self.license = license
        self.url = url

    def __str__(self):
        return "%s <%s>" % (self.name, self.url)

    @classmethod
    def all(klass):
        for line in open("datasets.csv"):
            line = line.strip()
            cols = line.split(",")
            yield Dataset(*cols)

    @property
    def triples_size(self):
        count = 0
        for t in self.triples():
            count += 1
        return count

    @property
    def size(self):
        r = requests.head(self.url)
        return int(r.headers['content-length'])

    @property 
    def download_file(self):
        return self.name + ".gz"

    def triples(self):
        if not os.path.isfile(self.download_file):
            self.download()
        for line in gzip.open(self.download_file):
            yield line

    def download(self):
        r = requests.get(self.url)
        f = open(self.download_file, "wb")
        for buff in r.iter_content(chunk_size=65536):
            f.write(buff)
        f.close()

if __name__ == "__main__":
    for ds in Dataset.all():
        if not os.path.isfile(ds.download_file):
            print "downloading: %s" % ds.download_file
            ds.download()
