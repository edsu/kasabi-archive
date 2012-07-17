The Kasabi data publishing platform created by Talis was <a href="">announced</a> to be closing on July 30, 2012.  While the service has only been around for ~2 years it represents a unique look at services for Linked Data, and contains a variety of datasets. In a subsequent [blog post](http://blog.kasabi.com/2012/07/16/archive-of-datasets/) Kasabi announced the availability of a spreadsheet that lists where datasets can be downloaded from Amazon S3.

kasabi-archive is a little one-off utility for downloading Kasabi data from s3 and putting it up at Internet Archive. Before you can run archive.py you will need to get Internet Archive [access keys](http://archive.org/account/s3.php) and add them to a .boto file in your home directory that looks like this:

    [Credentials]
    ia_access_key_id=[your-internet-archive-access-key]
    ia_secret_access_key=[your-internet-archive-secret-access-key]

Then follow these steps:

1. pip install -r requirements.txt
1. ./fetch.py
1. ./archive.py

The results are available at [http://archive.org/details/kasabi](http://archive.org/details/kasabi)
