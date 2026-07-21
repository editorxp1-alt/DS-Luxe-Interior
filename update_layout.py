import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add CSS
css_to_add = """
      /* 1. Floating Dock */
      .dock {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 50;
        display: flex;
        gap: 24px;
        background: oklch(16% 0.008 75 / 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 12px 32px;
        border-radius: 100px;
        border: 1px solid oklch(27% 0.012 78 / 0.5);
        box-shadow: 0 12px 32px oklch(0 0 0 / 0.5);
        transition: transform 0.3s var(--ease);
      }
      .dock:hover {
        transform: translateX(-50%) translateY(-4px);
      }
      .dock-item {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text);
        font-weight: 500;
        font-size: 15px;
        transition: color 0.2s;
      }
      .dock-item:hover { color: var(--gold); }
      .dock-item svg { width: 22px; height: 22px; fill: currentColor; }
      .dock-divider { width: 1px; height: 24px; background: var(--line); align-self: center; }
      
      /* 2. Materials Grid */
      .materials-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 24px;
        margin-top: 48px;
      }
      .material-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.3s var(--ease);
      }
      .material-card:hover { transform: translateY(-8px); }
      .material-img { height: 200px; overflow: hidden; }
      .material-img img { transition: transform 0.6s var(--ease); }
      .material-card:hover .material-img img { transform: scale(1.08); }
      .material-info { padding: 24px; }
      .material-info h3 { font-size: 20px; margin-bottom: 8px; font-family: var(--serif); font-weight: 500; }
      .material-info p { font-size: 14px; color: var(--muted); line-height: 1.5; }

      /* 3. Stories Grid */
      .stories-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 32px;
        margin-top: 48px;
      }
      .story-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
      }
      .story-video {
        height: 240px;
        position: relative;
        background: var(--panel2);
        cursor: pointer;
        overflow: hidden;
      }
      .story-video img { opacity: 0.85; transition: 0.4s var(--ease); }
      .story-card:hover .story-video img { opacity: 1; transform: scale(1.04); }
      .story-play {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
      }
      .story-play .play-btn {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: var(--gold);
        display: grid;
        place-items: center;
        box-shadow: 0 8px 24px oklch(0 0 0/0.4);
        transition: transform 0.3s var(--ease);
      }
      .story-card:hover .play-btn { transform: scale(1.1); }
      .story-play svg { width: 24px; height: 24px; fill: var(--bg); margin-left: 4px; }
      .story-content {
        padding: 32px 24px 24px;
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
      }
      .story-quote {
        font-style: italic;
        color: var(--text);
        font-size: 16px;
        line-height: 1.6;
        flex: 1;
      }
      .story-meta {
        display: flex;
        align-items: center;
        gap: 16px;
        border-top: 1px solid var(--line);
        padding-top: 20px;
      }
      .story-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        overflow: hidden;
        border: 2px solid var(--gold);
      }
      .story-author { font-size: 15px; }
      .story-author strong { display: block; color: var(--gold); font-weight: 600; }
      .story-author span { color: var(--muted); font-size: 13px; }
      .story-tags {
        position: absolute;
        top: 16px;
        left: 16px;
        display: flex;
        gap: 8px;
        z-index: 2;
      }
      .story-tag {
        background: oklch(12% 0.006 75 / 0.85);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: #fff;
        font-size: 11px;
        padding: 6px 10px;
        border-radius: 6px;
        border: 1px solid oklch(27% 0.012 78 / 0.5);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 600;
      }
"""

if "/* 1. Floating Dock */" not in content:
    content = content.replace('</style>', css_to_add + '\n    </style>')

materials_html = """
      <section class="section" id="materials">
        <div class="wrap">
          <div class="section-head reveal">
            <div class="eyebrow">The Palette</div>
            <h2>Premium Materials</h2>
            <p>We source only the finest authentic materials to ensure your space stands the test of time.</p>
          </div>
          <div class="materials-grid reveal">
            <div class="material-card">
              <div class="material-img">
                <img src="https://images.unsplash.com/photo-1600607688969-a5bfcd64bd28?auto=format&fit=crop&w=600&q=80" alt="Italian Marble">
              </div>
              <div class="material-info">
                <h3>Italian Marble</h3>
                <p>Luxurious, imported stones chosen for their unique veining and enduring elegance.</p>
              </div>
            </div>
            <div class="material-card">
              <div class="material-img">
                <img src="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=600&q=80" alt="Veneer Finishes">
              </div>
              <div class="material-info">
                <h3>Veneer Finishes</h3>
                <p>Natural wood grains treated with premium coatings for a rich, warm aesthetic.</p>
              </div>
            </div>
            <div class="material-card">
              <div class="material-img">
                <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=80" alt="Anti-scratch Acrylics">
              </div>
              <div class="material-info">
                <h3>Anti-scratch Acrylics</h3>
                <p>High-gloss, durable surfaces perfect for modern modular kitchens and seamless wardrobes.</p>
              </div>
            </div>
            <div class="material-card">
              <div class="material-img">
                <img src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80" alt="Premium Hardware">
              </div>
              <div class="material-info">
                <h3>Premium Hardware</h3>
                <p>Precision-engineered, soft-close fittings from leading European brands.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
"""

stories_html = """
      <section class="section" id="reviews">
        <div class="wrap">
          <div class="section-head reveal">
            <div class="eyebrow">Client stories</div>
            <h2>
              What living with<br /><span class="gold">good design feels like.</span>
            </h2>
            <p>Hear directly from the families and businesses who trusted us with their spaces.</p>
          </div>
          <div class="stories-grid reveal">
            <div class="story-card">
              <div class="story-video">
                <div class="story-tags">
                  <span class="story-tag">Gurugram</span>
                  <span class="story-tag">Full Home</span>
                </div>
                <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" alt="Video Thumbnail">
                <div class="story-play">
                  <div class="play-btn">
                    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
              </div>
              <div class="story-content">
                <div class="story-quote">
                  "The final home looks exactly like the approved render. Every material and detail feels intentional. The 3D previews were spot on."
                </div>
                <div class="story-meta">
                  <div class="story-avatar">
                    <img src="https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=100&q=80" alt="Ananya Mehta">
                  </div>
                  <div class="story-author">
                    <strong>Ananya Mehta</strong>
                    <span>3BHK Interior</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="story-card">
              <div class="story-video">
                <div class="story-tags">
                  <span class="story-tag">Noida</span>
                  <span class="story-tag">Kitchen</span>
                </div>
                <img src="https://images.unsplash.com/photo-1556910103-1c02745a872e?auto=format&fit=crop&w=600&q=80" alt="Video Thumbnail">
                <div class="story-play">
                  <div class="play-btn">
                    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
              </div>
              <div class="story-content">
                <div class="story-quote">
                  "Our kitchen is beautiful, but more importantly it works brilliantly every single day. The anti-scratch acrylics are a lifesaver."
                </div>
                <div class="story-meta">
                  <div class="story-avatar">
                    <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80" alt="Rohit Khanna">
                  </div>
                  <div class="story-author">
                    <strong>Rohit Khanna</strong>
                    <span>Modular Kitchen</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="story-card">
              <div class="story-video">
                <div class="story-tags">
                  <span class="story-tag">Delhi</span>
                  <span class="story-tag">Office</span>
                </div>
                <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=600&q=80" alt="Video Thumbnail">
                <div class="story-play">
                  <div class="play-btn">
                    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
              </div>
              <div class="story-content">
                <div class="story-quote">
                  "Clear updates, clean execution and no last-minute surprises. They transformed our bare commercial space into an inspiring workplace."
                </div>
                <div class="story-meta">
                  <div class="story-avatar">
                    <img src="https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?auto=format&fit=crop&w=100&q=80" alt="Vikram Rao">
                  </div>
                  <div class="story-author">
                    <strong>Vikram Rao</strong>
                    <span>Commercial Interior</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>
"""

# Replace old reviews section
if 'id="materials"' not in content:
    start_tag = '<section class="section" id="reviews">'
    old_reviews_start = content.find(start_tag)
    if old_reviews_start != -1:
        # find the next section
        next_section = content.find('<section class="section">', old_reviews_start + len(start_tag))
        if next_section != -1:
            content = content[:old_reviews_start] + materials_html + '\n' + stories_html + '\n      ' + content[next_section:]

dock_html = """
    <div class="dock reveal in">
      <a href="https://wa.me/919643168223" class="dock-item" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.663-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51h-.57c-.198 0-.52.074-.792.347-.272.273-1.04 1.015-1.04 2.476 0 1.46 1.065 2.871 1.213 3.07.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.086 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        WhatsApp
      </a>
      <div class="dock-divider"></div>
      <a href="tel:+919643168223" class="dock-item">
        <svg viewBox="0 0 24 24"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/></svg>
        Call Us
      </a>
    </div>
"""

float_start = content.find('<div class="float">')
if float_start != -1:
    # Find matching closing tag logic
    # Basically the old structure is:
    # <div class="float">
    #   <a ...>...</a>
    #   <a ...>...</a>
    # </div>
    float_end = content.find('</a></div>', float_start)
    if float_end != -1:
        content = content[:float_start] + dock_html + content[float_end+10:]
    else:
        # maybe formatted differently
        pass
else:
    # If not found, insert before <dialog
    dialog_idx = content.find('<dialog id="consultationModal">')
    if dialog_idx != -1:
        content = content[:dialog_idx] + dock_html + "\n    " + content[dialog_idx:]

with open('index.html', 'w') as f:
    f.write(content)

