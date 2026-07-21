import os

with open('server.ts', 'r') as f:
    content = f.read()

reviews_code = """
let reviewsData = [];
const reviewsPath = path.resolve('./reviews.json');
if (fs.existsSync(reviewsPath)) {
  try {
    reviewsData = JSON.parse(fs.readFileSync(reviewsPath, 'utf-8'));
  } catch (e) {
    console.error("Failed to parse local reviews data");
  }
}

app.get('/api/reviews', (req, res) => {
  res.json({ record: reviewsData });
});

app.post('/api/reviews', (req, res) => {
  const newReview = req.body;
  newReview.timestamp = Date.now();
  reviewsData.unshift(newReview);
  fs.writeFileSync(reviewsPath, JSON.stringify(reviewsData, null, 2));
  res.json({ success: true });
});
"""

if "app.get('/api/gallery'" in content:
    content = content.replace("app.get('/api/gallery'", reviews_code + "\napp.get('/api/gallery'")
    with open('server.ts', 'w') as f:
        f.write(content)
