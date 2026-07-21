import re

# Fix index.html
with open('index.html', 'r') as f:
    idx = f.read()

# 1. Remove reveal from homeReviewsGrid
idx = idx.replace('<div class="testimonials reveal" id="homeReviewsGrid">', '<div class="testimonials" id="homeReviewsGrid">')

# 2. Fix portraitImg error
idx = idx.replace('const portraitImg = document.querySelector(".portrait img");', 'const portraitImg = document.querySelector(".portrait video") || document.querySelector(".portrait img");')

# 3. Add styles to show them
with open('index.html', 'w') as f:
    f.write(idx)


# Fix reviews.html
with open('reviews.html', 'r') as f:
    rev = f.read()

# Remove 'reveal' class from the dynamically injected articles
rev = rev.replace('class="r-card reveal"', 'class="r-card"')

with open('reviews.html', 'w') as f:
    f.write(rev)

