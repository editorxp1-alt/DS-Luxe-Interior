import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.pexels.com/videos/search?query=luxury+interior+design+home&per_page=3"
req = urllib.request.Request(url, headers={'Authorization': '563492ad6f917000010000018a3832edff7a45ed9d8a1fc414c1ebbd'})

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        for video in data.get('videos', []):
            for f in video.get('video_files', []):
                if f.get('quality') == 'hd':
                    print(f.get('link'))
                    break
except Exception as e:
    print(e)
