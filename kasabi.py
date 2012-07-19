#!/usr/bin/env python

"""
Downloads the Kasabi dataset snapshots.
"""

import os
import sys
import boto
import gzip
import rdflib
import logging
import requests

from boto.s3.key import Key

class Dataset:
    _ia_bucket = None

    def __init__(self, name, license, url):
        self.name = name
        self.license = license
        self.url = url
        self.connect_ia()

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
    def ia_size(self):
        url = "http://archive.org/download/kasabi/" + self.ia_name
        r = requests.head(url, allow_redirects=True)
        return int(r.headers['content-length'])

    @property 
    def download_file(self):
        return self.name + ".gz"

    @property
    def named_graph_file(self):
        return self.name + ".nt"

    @property
    def ia_name(self):
        return self.download_file.replace("dataset/", "")

    @property
    def ia_named_graph_name(self):
        return self.download_file.replace("dataset/", "").replace(".gz", ".nt")

    @property
    def downloaded(self):
        return os.path.isfile(ds.download_file)

    @property
    def archived(self):
        return self.get_ia_key() != None

    @property
    def named_graph_url(self):
        """guesses the named graph URI for the dataset by taking the first one
        """
        for quad in self.triples():
            u = quad.split(" ")[-2].strip("<").strip(">")
            if u.startswith("http://data.kasabi.com"):
                return u
            return None

    @property
    def named_graph(self):
        g = rdflib.Graph()
        u = self.named_graph_url
        # apparently not all datasets are quads :-/
        if not u:
            return None
        try:
            return g.parse(u)
        except Exception, e:
            logging.error("unable to get named graph url %s: %s", u, e)

    def get_ia_key(self):
        return Dataset._ia_bucket.get_key(self.ia_name)

    def get_ia_named_graph_key(self):
        return Dataset._oa_bucket.get_eky(self.ia_named_graph_name)

    def triples(self):
        if not os.path.isfile(self.download_file):
            self.download()
        for line in gzip.open(self.download_file):
            yield line

    def download(self):
        logging.info("downloading: %s", ds.download_file)
        r = requests.get(self.url)
        f = open(self.download_file, "wb")
        for buff in r.iter_content(chunk_size=65536):
            f.write(buff)
        f.close()
        self.download_named_graph()

    def download_named_graph(self):
        g = self.named_graph
        if not g:
            logging.info("unable to download named graph for %s", self)
            return None
        logging.info("saving named graph for %s as %s", self, self.named_graph_file)
        g.serialize(open(self.named_graph_file, "w"), format="nt")

    def archive(self):
        self.archive_dataset()
        self.archive_named_graph()

    def archive_dataset(self):
        k = self.get_ia_key()
        if not k:
            k = Key(Dataset._ia_bucket)
            k.name = self.ia_name
            k.set_contents_from_filename(self.download_file)

    def archive_named_graph(self):
        if self.named_graph:
            logging.info("archiving named graph %s as %s", self, self.ia_named_graph_name)
            k = Key(Dataset._ia_bucket)
            k.name = self.ia_named_graph_name
            k.set_contents_from_filename(self.named_graph_file)
        else:
            logging.warn("no named graph for %s", self)

    def connect_ia(self):
        if not Dataset._ia_bucket:
            ia = boto.connect_ia()
            try:
                Dataset._ia_bucket = ia.get_bucket("kasabi")
            except:
                Dataset._ia__bucket = ia.create_bucket("kasabi")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    for ds in Dataset.all():
        if not ds.downloaded:
            print "downloading %s" % ds
            ds.download()
        if not ds.archived:
            print "archiving %s" % ds
            logging.info("archiving: %s", ds)
            ds.archive()
