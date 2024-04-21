# Metadata
challenge metadata is stored in the top level of each challenge (where challenge.yaml is stored) and must contain the following:

``` yaml
name: str
description: str
flag: UMASS{str}
```
It can also optionally contain the following values to override defaults:
``` yaml
category: str
points:
    initial: num
    function: 'linear' | 'logarithmic'
    decay: num
    minimum: num
wave: num
state: 'hidden' | 'visible'
ignore: True | False # This will prevent the script from updating the challenge (use if you want to make manual changes)
requirements:
    anonymize: True | False
    prerequisites: [challenge names...]
tags: [tag values...]
```
# Tools
Tools and data are stored in the [tools](./) folder. There you should also have a .env file to store access tokens and other configurations.
## Metadata
There is a [metadata.py](./metadata.py) script that contains utility functions and can also generate a json file that contains all challenge metadata. In order to use it, set the following values in the configuration file:
```
BASE_PATH = "../" # Relative path to script location
CATEGORIES = 'crypto,misc,rev,rf,web' # The folders it will search in
```
## Upload
There is an [upload_challenges.py](./upload_challenges.py) script that automaticlly takes the metadata and uploads it to CTFd. In order to use it, set the following values in the configuration file:
```
URL = "https://ctf.umasscybersec.org" # url for CTFd server
TOKEN = "your-access-token"  # access token for CTFd server
BUCKET_NAME = "test" # name of the gcp bucket that has static files (do not put the whole url)
```

NOTE: The upload script currently can not get challenges from CTFd so it creates and updates an uploaded.json file to keep track of challenge id's. The script needs this file to tell which challenges are already uploaded and which need to be created. If this file is deleted or modified, it may duplicate challenges.
