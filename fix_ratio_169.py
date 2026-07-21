import re

with open('index.html', 'r') as f:
    content = f.read()

# Change to 16/9
content = content.replace('aspect-ratio: 4 / 5;', 'aspect-ratio: 16 / 9;')
content = content.replace('aspect-ratio: 4 / 3;', 'aspect-ratio: 16 / 9;')

with open('index.html', 'w') as f:
    f.write(content)
