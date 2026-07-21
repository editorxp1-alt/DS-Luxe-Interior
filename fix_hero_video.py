import re

with open('index.html', 'r') as f:
    content = f.read()

# Remove the hero iframe and replace it
content = re.sub(r'<div class="hero-bg-video">\s*<iframe.*?</iframe>\s*</div>',
                 r'<div class="hero-bg-video">\n          <video src="https://www.shutterstock.com/shutterstock/videos/1063991206/preview/stock-footage-luxury-modern-living-room-interior-with-panoramic-windows-and-a-beautiful-view-of-the-ocean-and.mp4" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover;"></video>\n        </div>', content)

# Remove the portrait iframe and replace it
content = re.sub(r'<div class="vid-wrap">\s*<iframe.*?</iframe>\s*</div>',
                 r'<div class="vid-wrap">\n              <video src="https://www.shutterstock.com/shutterstock/videos/1105953931/preview/stock-footage-modern-interior-design-of-the-living-room-with-kitchen-and-dining-room-d-animation-video.mp4" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover;"></video>\n            </div>', content, count=1)

# Remove the project iframe and replace it
content = re.sub(r'<div class="vid-wrap">\s*<iframe.*?</iframe>\s*</div>',
                 r'<div class="vid-wrap">\n                <video src="https://www.shutterstock.com/shutterstock/videos/1054921607/preview/stock-footage-empty-modern-interior-with-panoramic-windows-and-city-view-d-animation.mp4" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover;"></video>\n              </div>', content, count=1)

with open('index.html', 'w') as f:
    f.write(content)
