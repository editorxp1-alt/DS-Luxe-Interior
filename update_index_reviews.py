import re

with open('index.html', 'r') as f:
    content = f.read()

testimonials_html_old = """          <div class="testimonials reveal">
            <article class="quote">
              <div>
                <div class="stars">★★★★★</div>
                <blockquote>
                  “The final home looks exactly like the approved render. Every
                  material and detail feels intentional.”
                </blockquote>
              </div>
              <div><b>Ananya Mehta</b><small>Full home, Gurugram</small></div>
            </article>
            <article class="quote">
              <div>
                <div class="stars">★★★★★</div>
                <blockquote>
                  “Our kitchen is beautiful, but more importantly it works
                  brilliantly every single day.”
                </blockquote>
              </div>
              <div>
                <b>Rohit Khanna</b><small>Modular kitchen, Noida</small>
              </div>
            </article>
            <article class="quote">
              <div>
                <div class="stars">★★★★★</div>
                <blockquote>
                  “Clear updates, clean execution and no last-minute surprises.”
                </blockquote>
              </div>
              <div>
                <b>Vikram Rao</b><small>Office interior, Gurugram</small>
              </div>
            </article>
          </div>"""

testimonials_html_new = """          <div class="testimonials reveal" id="homeReviewsGrid">
            <!-- Dynamically loaded reviews will go here -->
          </div>
          <div style="margin-top: 40px; text-align: center;" id="seeMoreReviewsBtn">
            <a href="reviews.html" class="btn" style="background: transparent; border: 1px solid var(--line);">See all reviews</a>
          </div>"""

if testimonials_html_old in content:
    content = content.replace(testimonials_html_old, testimonials_html_new)
else:
    print("WARNING: Old testimonials block not found")

# Let's add JS to fetch the reviews on index.html
js_to_add = """
      async function loadHomeReviews() {
        const grid = document.getElementById('homeReviewsGrid');
        if(!grid) return;
        try {
          const res = await fetch('/api/reviews');
          if (!res.ok) throw new Error('Failed');
          const data = await res.json();
          const reviews = data.record || [];
          
          if(reviews.length > 0) {
            let html = '';
            // Show only first 3 reviews
            reviews.slice(0, 3).forEach(r => {
              const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
              html += `
                <article class="quote">
                  <div>
                    <div class="stars">${stars}</div>
                    <blockquote>"${r.review}"</blockquote>
                  </div>
                  <div><b>${r.name}</b><small>${r.location}</small></div>
                </article>
              `;
            });
            grid.innerHTML = html;
          }
          
          if(reviews.length <= 3) {
            const btn = document.getElementById('seeMoreReviewsBtn');
            if(btn) btn.style.display = 'none';
          }
        } catch(e) {
          console.error(e);
        }
      }
      loadHomeReviews();
"""
# Insert before </script>
script_end_idx = content.rfind('</script>')
if script_end_idx != -1:
    content = content[:script_end_idx] + js_to_add + content[script_end_idx:]

# Also update the submit handler to push to our backend AND web3forms
# Currently it looks like:
#      document.getElementById('reviewForm').onsubmit = (e) => {
#        e.preventDefault();
#        const f = e.target;
#        if (!f.checkValidity()) return f.reportValidity();
#        const d = new FormData(f);
#        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
#        d.append("subject", "New Client Review Submitted - DS Luxe");
#        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
#        document.getElementById('reviewFormWrap').style.display = "none";
#        document.getElementById('reviewSuccess').style.display = "block";
#      };

old_review_submit = """        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });"""
new_review_submit = """        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        // Also save to our local backend
        const reviewData = {
          name: d.get('Name'),
          location: d.get('Location'),
          rating: parseInt(d.get('Rating')),
          review: d.get('Review')
        };
        fetch('/api/reviews', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(reviewData)
        }).then(() => {
          loadHomeReviews(); // reload reviews
        });"""

content = content.replace(old_review_submit, new_review_submit)

with open('index.html', 'w') as f:
    f.write(content)

