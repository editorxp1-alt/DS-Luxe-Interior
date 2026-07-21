import re

with open('reviews.html', 'r') as f:
    content = f.read()

# The script block
script_pattern = re.compile(r'<script>.*?</script>', re.DOTALL)
scripts = script_pattern.findall(content)

# The dialog block
dialog_pattern = re.compile(r'<dialog id="reviewModal">.*?</dialog>', re.DOTALL)
dialogs = dialog_pattern.findall(content)

if len(scripts) > 0 and len(dialogs) > 0:
    content = content.replace(dialogs[0], '')
    content = content.replace(scripts[0], dialogs[0] + '\n' + scripts[0])

with open('reviews.html', 'w') as f:
    f.write(content)
