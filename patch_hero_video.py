import re

with open('index.html', 'r') as f:
    content = f.read()

css_old = """      .hero {
        min-height: 100vh;
        position: relative;
        display: grid;
        align-items: end;
        padding: 150px 0 80px;
        background-image:
          linear-gradient(
            90deg,
            oklch(8% 0.006 75/0.94),
            oklch(8% 0.006 75/0.72) 48%,
            oklch(8% 0.006 75/0.2)
          ),
          url("https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=2000&q=88");
        background-size: cover;
        background-position: center;
      }"""

css_new = """      .hero {
        min-height: 100vh;
        position: relative;
        display: grid;
        align-items: end;
        padding: 150px 0 80px;
        background-color: oklch(8% 0.006 75);
        overflow: hidden;
      }
      .hero-bg-video {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
      }
      .hero-bg-video iframe {
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
      }
      .hero .wrap {
        position: relative;
        z-index: 1;
      }"""

content = content.replace(css_old, css_new)

hero_old = """      <section class="hero" id="home">
        <div class="wrap">"""

hero_new = """      <section class="hero" id="home">
        <div class="hero-bg-video">
          <iframe src="https://www.youtube.com/embed/BCPgdQ_6cyg?autoplay=1&mute=1&loop=1&playlist=BCPgdQ_6cyg&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
        <div class="hero-gradient" style="position:absolute; inset:0; z-index:0; background: linear-gradient(90deg, oklch(8% 0.006 75/0.94), oklch(8% 0.006 75/0.72) 48%, oklch(8% 0.006 75/0.2)); pointer-events: none;"></div>
        <div class="wrap">"""

content = content.replace(hero_old, hero_new)

with open('index.html', 'w') as f:
    f.write(content)
