import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://api.jsonbin.io/v3/b/6a5772b4da38895dfe60ab40")
req.add_header("X-Master-Key", "$2a$10$dySlyKWtDmqIrrOcquURWeinFotbSXwgwZHeC6Bqu9RHcaE5T5KWu")
with urllib.request.urlopen(req, context=ctx) as response:
    data = json.loads(response.read().decode())

broken = []
for item in data.get("record", []):
    for img in item.get("images", []):
        try:
            r = urllib.request.urlopen(urllib.request.Request(img, method='HEAD'), context=ctx, timeout=5)
            # wait, postimg might return 200 for "image removed" placeholder
            # let's download the first 100 bytes and see if it redirects or has a specific signature
            # Actually postimg returns 200 for the placeholder image.
            # Let's check Content-Length.
        except Exception as e:
            broken.append((img, str(e)))

print("HTTP Errors:", broken)
