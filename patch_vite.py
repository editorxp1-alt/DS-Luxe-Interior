with open('vite.config.ts', 'r') as f:
    content = f.read()

content = content.replace("gallery: path.resolve(__dirname, 'gallery.html')", "gallery: path.resolve(__dirname, 'gallery.html'),\n          reviews: path.resolve(__dirname, 'reviews.html')")

with open('vite.config.ts', 'w') as f:
    f.write(content)
