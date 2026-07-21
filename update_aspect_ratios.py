import re

with open('index.html', 'r') as f:
    content = f.read()

css_hero_old = """      .hero-bg-video video {
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

css_hero_new = """      .hero-bg-video video, .hero-bg-video iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        opacity: 0.55;
        border: none;
      }"""
content = content.replace(css_hero_old, css_hero_new)

# Update portrait to a vertical aspect ratio
css_port_old = """      .portrait {
        height: 650px;
        position: relative;
        overflow: hidden;
      }"""
css_port_new = """      .portrait {
        aspect-ratio: 4 / 5;
        height: auto;
        position: relative;
        overflow: hidden;
      }"""
content = content.replace(css_port_old, css_port_new)

# Update project to a standard aspect ratio
css_proj_old = """      .project {
        position: relative;
        overflow: hidden;
        min-height: 620px;
      }"""
css_proj_new = """      .project {
        position: relative;
        overflow: hidden;
        aspect-ratio: 4 / 3;
        height: auto;
      }"""
content = content.replace(css_proj_old, css_proj_new)

css_small_old = """      .project.small {
        min-height: 301px;
      }"""
css_small_new = """      .project.small {
        aspect-ratio: 4 / 3;
        height: auto;
      }"""
content = content.replace(css_small_old, css_small_new)


with open('index.html', 'w') as f:
    f.write(content)
