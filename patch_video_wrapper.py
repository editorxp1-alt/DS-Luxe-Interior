import re

with open('index.html', 'r') as f:
    content = f.read()

css_old = """      .portrait {
        height: 650px;
        position: relative;
        overflow: hidden;
      }"""

css_new = """      .portrait {
        height: 650px;
        position: relative;
        overflow: hidden;
      }
      .vid-wrap {
        position: absolute; inset: 0; overflow: hidden; pointer-events: none;
      }
      .vid-wrap iframe {
        position: absolute; top: 50%; left: 50%;
        width: 250%; height: 250%;
        transform: translate(-50%, -50%);
        border: none;
      }"""

content = content.replace(css_old, css_new)

# Update portrait
portrait_old = """          <div class="portrait reveal" style="pointer-events: none;">
            <iframe src="https://www.youtube.com/embed/L4zmrEc4PCY?autoplay=1&mute=1&loop=1&playlist=L4zmrEc4PCY&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen style="width: 100%; height: 100%; border: none; object-fit: cover;"></iframe>
          </div>"""

portrait_new = """          <div class="portrait reveal">
            <div class="vid-wrap">
              <iframe src="https://www.youtube.com/embed/L4zmrEc4PCY?autoplay=1&mute=1&loop=1&playlist=L4zmrEc4PCY&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
          </div>"""
content = content.replace(portrait_old, portrait_new)


# Update first project with another luxury video short (maybe user's BCPgdQ_6cyg)
project_old = """            <article class="project">
              <img decoding="async" loading="lazy"
                src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1300&q=86"
                alt="Contemporary luxury living room"
              />"""

project_new = """            <article class="project">
              <div class="vid-wrap">
                <iframe src="https://www.youtube.com/embed/BCPgdQ_6cyg?autoplay=1&mute=1&loop=1&playlist=BCPgdQ_6cyg&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>
              </div>"""
content = content.replace(project_old, project_new)

with open('index.html', 'w') as f:
    f.write(content)

