import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.jsonbin.io/v3/b/6a5772b4da38895dfe60ab40"
headers = {"X-Master-Key": "$2a$10$dySlyKWtDmqIrrOcquURWeinFotbSXwgwZHeC6Bqu9RHcaE5T5KWu"}
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if 'record' in data:
            with open('gallery-data.json', 'w') as f:
                json.dump(data['record'], f, indent=2)
            print("Downloaded successfully")
        else:
            print("No record found in jsonbin response")
except Exception as e:
    print(f"Error downloading: {e}")
