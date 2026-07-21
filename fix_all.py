import re

# 1. Update index.html
with open('index.html', 'r') as f:
    idx = f.read()

# Replace hero youtube iframe with video tag
hero_old = '<iframe src="https://www.youtube.com/embed/BCPgdQ_6cyg?autoplay=1&mute=1&loop=1&playlist=BCPgdQ_6cyg&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
hero_new = '<video src="https://www.shutterstock.com/shutterstock/videos/1063991206/preview/stock-footage-luxury-modern-living-room-interior-with-panoramic-windows-and-a-beautiful-view-of-the-ocean-and.mp4" autoplay loop muted playsinline class="hero-vid" style="width: 100vw; height: 100vh; object-fit: cover; opacity: 0.8;"></video>'
idx = idx.replace(hero_old, hero_new)

# Fix hero css for video
hero_css_old = """      .hero-bg-video iframe {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100vw;
        height: 177.77vw;
        min-height: 100vh;
        min-width: 56.25vh;
        transform: translate(-50%, -50%);
        opacity: 0.55;
        border: none;
      }"""
hero_css_new = """      .hero-bg-video video {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        transform: translate(-50%, -50%);
        opacity: 0.55;
        border: none;
      }"""
idx = idx.replace(hero_css_old, hero_css_new)


# Replace portrait youtube iframe with video tag
port_old = '<iframe src="https://www.youtube.com/embed/L4zmrEc4PCY?autoplay=1&mute=1&loop=1&playlist=L4zmrEc4PCY&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
port_new = '<video src="https://www.shutterstock.com/shutterstock/videos/1105953931/preview/stock-footage-modern-interior-design-of-the-living-room-with-kitchen-and-dining-room-d-animation-video.mp4" autoplay loop muted playsinline style="width: 100%; height: 100%; object-fit: cover;"></video>'
idx = idx.replace(port_old, port_new)

# Replace project youtube iframe with video tag
proj_old = '<iframe src="https://www.youtube.com/embed/BCPgdQ_6cyg?autoplay=1&mute=1&loop=1&playlist=BCPgdQ_6cyg&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
proj_new = '<video src="https://www.shutterstock.com/shutterstock/videos/1054921607/preview/stock-footage-empty-modern-interior-with-panoramic-windows-and-city-view-d-animation.mp4" autoplay loop muted playsinline style="width: 100%; height: 100%; object-fit: cover;"></video>'
idx = idx.replace(proj_old, proj_new)

# Fix video wrappers in CSS
vid_css_old = """      .vid-wrap iframe {
        position: absolute; top: 50%; left: 50%;
        width: 250%; height: 250%;
        transform: translate(-50%, -50%);
        border: none;
      }"""
vid_css_new = """      .vid-wrap video {
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        border: none;
      }"""
idx = idx.replace(vid_css_old, vid_css_new)


# Fix fetch cache in index.html
fetch_old = "const res = await fetch('/api/reviews');"
fetch_new = "const res = await fetch('/api/reviews', { cache: 'no-store' });"
idx = idx.replace(fetch_old, fetch_new)

with open('index.html', 'w') as f:
    f.write(idx)


# 2. Update reviews.html
with open('reviews.html', 'r') as f:
    rev = f.read()

# Fix fetch cache in reviews.html
rev = rev.replace(fetch_old, fetch_new)

with open('reviews.html', 'w') as f:
    f.write(rev)

