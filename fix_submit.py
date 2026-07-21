import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix Contact form (form.onsubmit)
contact_old = """      form.onsubmit = (e) => {
        e.preventDefault();
        if (!form.checkValidity()) return form.reportValidity();
        const d = new FormData(form);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Inquiry - DS Luxe");
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
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
        });
        formFields.style.display = "none";
        success.style.display = "block";
      };"""

contact_new = """      form.onsubmit = (e) => {
        e.preventDefault();
        if (!form.checkValidity()) return form.reportValidity();
        const d = new FormData(form);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Inquiry - DS Luxe");
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        formFields.style.display = "none";
        success.style.display = "block";
      };"""
content = content.replace(contact_old, contact_new)

# Fix Consultation form
consult_old = """      consultationForm.onsubmit = (e) => {
        e.preventDefault();
        if (!consultationForm.checkValidity())
          return consultationForm.reportValidity();
        const d = new FormData(consultationForm);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Consultation Booking - DS Luxe");
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
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
        });
        modalFormWrap.style.display = "none";
        modalSuccess.style.display = "block";
      };"""

consult_new = """      consultationForm.onsubmit = async (e) => {
        e.preventDefault();
        if (!consultationForm.checkValidity())
          return consultationForm.reportValidity();
        const d = new FormData(consultationForm);
        d.append("access_key", "7c681d79-a9b4-46c6-8a9e-6c91bc5537e1");
        d.append("subject", "New Consultation Booking - DS Luxe");
        
        // Handle images if any
        const refImages = d.getAll('Reference_Images');
        if (refImages && refImages.length > 0 && refImages[0].size > 0) {
          // Send to local upload endpoint so it gets a URL, then include in web3forms
          let urls = [];
          for (let img of refImages) {
            const fd = new FormData();
            fd.append('image', img);
            try {
               const res = await fetch('/api/upload', {method: 'POST', body: fd});
               const json = await res.json();
               if(json.success && json.data.url) urls.push(window.location.origin + json.data.url);
            } catch(err) {}
          }
          if (urls.length > 0) {
            d.append('Reference_Links', urls.join(', '));
            d.delete('Reference_Images'); // web3forms doesn't handle pure files as well without multipart
          }
        }
        
        fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        modalFormWrap.style.display = "none";
        modalSuccess.style.display = "block";
      };"""

content = content.replace(consult_old, consult_new)

with open('index.html', 'w') as f:
    f.write(content)

