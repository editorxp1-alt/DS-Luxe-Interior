import re

with open('reviews.html', 'r') as f:
    content = f.read()

# Add Review Modal HTML to reviews.html
review_modal_html = """
    <dialog id="reviewModal">
      <div id="reviewFormWrap">
        <div class="modal-head">
          <button class="modal-close" onclick="document.getElementById('reviewModal').close(); document.body.classList.remove('lock');" aria-label="Close">
            ×
          </button>
          <div class="eyebrow">Client Feedback</div>
          <h2>Share your experience</h2>
          <p>We'd love to hear about your journey with DS Luxe.</p>
        </div>
        <form class="modal-form" id="reviewForm">
          <div class="form-grid">
            <div class="field">
              <label>Name</label><input name="Name" required />
            </div>
            <div class="field">
              <label>Location / Project Type</label><input name="Location" required />
            </div>
            <div class="field" style="grid-column: 1 / -1;">
              <label>Rating</label>
              <select name="Rating" required>
                <option value="5">★★★★★ (5/5)</option>
                <option value="4">★★★★☆ (4/5)</option>
                <option value="3">★★★☆☆ (3/5)</option>
                <option value="2">★★☆☆☆ (2/5)</option>
                <option value="1">★☆☆☆☆ (1/5)</option>
              </select>
            </div>
            <div class="field" style="grid-column: 1 / -1;">
              <label>Your Review</label>
              <textarea name="Review" required style="width:100%;height:100px;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:12px;color:var(--text);font-family:inherit;"></textarea>
            </div>
          </div>
          <button type="submit" class="btn" style="width: 100%; margin-top: 24px;">Submit Review</button>
        </form>
      </div>
      <div id="reviewSuccess" style="display: none; text-align: center; padding: 40px 0;">
        <div style="font-size: 48px; margin-bottom: 24px;">✨</div>
        <h2>Thank You!</h2>
        <p>Your review has been submitted successfully.</p>
        <button class="btn" style="margin-top: 32px;" onclick="document.getElementById('reviewModal').close(); document.body.classList.remove('lock');">Close</button>
      </div>
    </dialog>
"""

# Insert modal
body_close_idx = content.find('</body>')
if body_close_idx != -1:
    content = content[:body_close_idx] + review_modal_html + "\n  " + content[body_close_idx:]

# Add Write a Review button to the hero section
hero_idx = content.find('<p class="g-count" id="itemCount">Loading reviews...</p>')
if hero_idx != -1:
    insert_str = '\n      <button class="btn" style="margin-top: 20px;" onclick="document.getElementById(\'reviewModal\').showModal(); document.body.classList.add(\'lock\');">Write a Review</button>'
    insert_pos = hero_idx + len('<p class="g-count" id="itemCount">Loading reviews...</p>')
    content = content[:insert_pos] + insert_str + content[insert_pos:]

# Add js for reviewForm
js_str = """
      document.getElementById('reviewForm').onsubmit = (e) => {
        e.preventDefault();
        const f = e.target;
        if (!f.checkValidity()) return f.reportValidity();
        const d = new FormData(f);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Client Review Submitted - DS Luxe");
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        
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
          loadReviews();
        });
        
        document.getElementById('reviewFormWrap').style.display = "none";
        document.getElementById('reviewSuccess').style.display = "block";
      };
"""

js_idx = content.find('loadReviews();')
if js_idx != -1:
    insert_pos = js_idx + len('loadReviews();')
    content = content[:insert_pos] + js_str + content[insert_pos:]

with open('reviews.html', 'w') as f:
    f.write(content)

