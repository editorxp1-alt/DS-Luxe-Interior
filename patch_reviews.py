import re

with open('reviews.html', 'r') as f:
    content = f.read()

# Replace header text
content = content.replace('<div class="eyebrow">DS Luxe — Portfolio</div>', '<div class="eyebrow">DS Luxe — Reviews</div>')
content = content.replace('<h1 id="svcName">Loading…</h1>', '<h1 id="svcName">Client Stories</h1>')
content = content.replace('<p class="g-count" id="itemCount"></p>', '<p class="g-count" id="itemCount">Loading reviews...</p>')

# Replace CSS
css_old = """      .g-grid {
        padding: 46px clamp(20px, 4vw, 60px);
        columns: 4 260px;
        column-gap: 14px;
      }"""
css_new = """      .r-grid {
        padding: 46px clamp(20px, 4vw, 60px);
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 24px;
        max-width: 1400px;
        margin: 0 auto;
      }
      .r-card {
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 30px;
        background: var(--panel);
        transition: 0.4s var(--ease);
      }
      .r-card:hover {
        border-color: var(--gold);
        transform: translateY(-2px);
      }
      .r-stars { color: var(--gold); margin-bottom: 16px; font-size: 14px; letter-spacing: 2px;}
      .r-text { font-family: 'Cormorant Garamond', serif; font-size: 24px; line-height: 1.3; margin-bottom: 24px; font-style: italic; color: var(--text); }
      .r-author { font-weight: 600; font-size: 15px; color: var(--text); }
      .r-loc { font-size: 13px; color: var(--muted); margin-top: 4px; }
"""
content = content.replace(css_old, css_new)

# Replace Grid HTML
grid_old = """    <div id="gGrid" class="g-grid"></div>
    <div class="g-empty" id="gEmpty">
      <div class="g-empty-icon">🖼️</div>
      <h2>Gallery Coming Soon</h2>
      <p>
        Our team is curating beautiful images and videos for this service.
        Please check back soon.
      </p>
    </div>"""

grid_new = """    <div id="rGrid" class="r-grid"></div>
    <div class="g-empty" id="gEmpty" style="display:none;">
      <div class="g-empty-icon">💬</div>
      <h2>No reviews yet</h2>
      <p>Be the first to share your experience with DS Luxe.</p>
    </div>"""
content = content.replace(grid_old, grid_new)

# Replace JS script
js_start = content.find('<script>')
js_end = content.find('</script>') + len('</script>')

new_js = """<script>
      async function loadReviews() {
        const grid = document.getElementById('rGrid');
        const empty = document.getElementById('gEmpty');
        const count = document.getElementById('itemCount');
        
        try {
          const res = await fetch('/api/reviews');
          if (!res.ok) throw new Error('Failed to fetch');
          const data = await res.json();
          const reviews = data.record || [];
          
          if (reviews.length === 0) {
            empty.style.display = 'flex';
            count.textContent = '0 reviews';
            return;
          }
          
          count.textContent = `${reviews.length} ${reviews.length === 1 ? 'review' : 'reviews'}`;
          
          let html = '';
          reviews.forEach((r, i) => {
            const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
            html += `
              <article class="r-card reveal" style="animation: fadeUp 0.8s var(--ease) ${i * 0.1}s forwards; opacity: 0;">
                <div class="r-stars">${stars}</div>
                <div class="r-text">"${r.review}"</div>
                <div class="r-author">${r.name}</div>
                <div class="r-loc">${r.location}</div>
              </article>
            `;
          });
          grid.innerHTML = html;
        } catch (err) {
          console.error(err);
          empty.style.display = 'flex';
          empty.querySelector('h2').textContent = 'Error';
          empty.querySelector('p').textContent = 'Could not load reviews at this time.';
          count.textContent = '';
        }
      }
      loadReviews();
    </script>"""

content = content[:js_start] + new_js + content[js_end:]

# Replace lightbox HTML (not needed for reviews)
lb_start = content.find('<!-- Lightbox -->')
lb_end = content.find('</div>\n    <script>', lb_start)
if lb_end == -1:
    lb_end = content.find('<script>', lb_start)
content = content[:lb_start] + content[lb_end:]


with open('reviews.html', 'w') as f:
    f.write(content)
