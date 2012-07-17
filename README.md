kasabi-archive is a little one-off utility for downloading Kasabi data from s3 
and putting it up at Internet Archive. Before you can run archive.py you will 
need to get Internet Archive [access keys](http://archive.org/account/s3.php) 
and add them to a .boto file in your home directory that looks like this:

    [Credentials]
    ia_access_key_id=[your-internet-archive-access-key]
    ia_secret_access_key=[your-internet-archive-secret-access-key]

Then follow these steps:

1. pip install -r requirements.txt
1. ./fetch.py
1. ./archive.py

The results are available at [http://archive.org/details/kasabi](http://archive.org/details/kasabi)
