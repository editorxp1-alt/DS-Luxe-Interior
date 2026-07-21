import re

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # For gallery.html
    old_fetch = """          const res = await fetch(GET_URL, {
            headers: { 'X-Master-Key': JSONBIN_KEY }
          });"""
    new_fetch = """          const res = await fetch('/api/gallery');"""
    
    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch)

    # For admin.html
    admin_fetch_old = """      const res = await fetch(GET_URL, {
        headers: {
          'X-Master-Key': JSONBIN_KEY
        }
      });"""
    admin_fetch_new = """      const res = await fetch('/api/gallery');"""
    if admin_fetch_old in content:
        content = content.replace(admin_fetch_old, admin_fetch_new)

    admin_put_old = """      const res = await fetch(PUT_URL, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Master-Key": JSONBIN_KEY
        },
        body: JSON.stringify(appData)
      });"""
    admin_put_new = """      const res = await fetch('/api/gallery', {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(appData)
      });"""
    if admin_put_old in content:
        content = content.replace(admin_put_old, admin_put_new)

    with open(filepath, 'w') as f:
        f.write(content)

update_file('gallery.html')
update_file('admin.html')

