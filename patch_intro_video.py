import re

with open('index.html', 'r') as f:
    content = f.read()

portrait_old = """          <div class="portrait reveal">
            <img decoding="async" loading="lazy"
              src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1000&q=86"
              alt="Warm luxury living room"
              style="transform: scale(1.15); transform-origin: top center;"
            />
          </div>"""

portrait_new = """          <div class="portrait reveal" style="pointer-events: none;">
            <iframe src="https://www.youtube.com/embed/L4zmrEc4PCY?autoplay=1&mute=1&loop=1&playlist=L4zmrEc4PCY&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen style="width: 100%; height: 100%; border: none; object-fit: cover;"></iframe>
          </div>"""

content = content.replace(portrait_old, portrait_new)

with open('index.html', 'w') as f:
    f.write(content)

