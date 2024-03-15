# chilicloud

A simple api wrapper for Chilicloud. A package that allows you to interact with your Chilicloud account using the Chilicloud API. You can upload, download and delete files.

Install from pypi: `python3 -m pip install chilicloud`

---

## Warning!

This project was created for fun and hasn't undergone extensive testing. Please use it responsibly and at your own risk.

---

### Example:

```python
from chilicloud.chilicloud import *

updateApiToken() # Gets a new X-Apigw-Session token for interacting with the API
file_uuid = uploadFile('test_file.txt') # Uploads out test_file.txt to the server
downloadFile(file_uuid, 'downloaded_file.txt') # Retrieves the uploaded file
deleteFile(file_uuid) # Deletes the uploaded file
```

---

### The idea

I wanted to use the chilicloud service but I dont like their Sync Client, so I explored the api calls and made this.

I also wanted to implement a encrypt and split files feature, to split a file into file.part1, file.part2..... And then encrypt each part file for extra security.