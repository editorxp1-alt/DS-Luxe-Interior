import re

with open('index.html', 'r') as f:
    content = f.read()

# Add Write Review button next to "What living with good design feels like"
btn_html = """
          </div>
          <div style="margin-top:20px;text-align:center;">
            <button class="btn" onclick="document.getElementById('reviewModal').showModal(); document.body.classList.add('lock');">Write a Review</button>
          </div>
          <div class="stories-grid reveal">
"""
content = content.replace('</div>\n          <div class="stories-grid reveal">', btn_html)

# Add Review Modal HTML before consultationModal
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
              <label>Location / Project Type (e.g. Noida, Kitchen)</label><input name="Location" required />
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

content = content.replace('<dialog id="consultationModal">', review_modal_html + '\n    <dialog id="consultationModal">')

# Add JS handler for reviewForm
js_to_add = """
      document.getElementById('reviewForm').onsubmit = (e) => {
        e.preventDefault();
        const f = e.target;
        if (!f.checkValidity()) return f.reportValidity();
        const d = new FormData(f);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Client Review Submitted - DS Luxe");
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        document.getElementById('reviewFormWrap').style.display = "none";
        document.getElementById('reviewSuccess').style.display = "block";
      };
"""

content = content.replace('consultationForm.onsubmit = (e) => {', js_to_add + '\n      consultationForm.onsubmit = (e) => {')

with open('index.html', 'w') as f:
    f.write(content)

