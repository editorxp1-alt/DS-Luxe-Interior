const fs = require('fs');
const html = fs.readFileSync('reviews.html', 'utf8');
const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (scriptMatch) {
  try {
    new Function(scriptMatch[1]);
    console.log("JS in reviews.html is valid");
  } catch (e) {
    console.log("Syntax error in reviews.html JS:", e);
  }
}
