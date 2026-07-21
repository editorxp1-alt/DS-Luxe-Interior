import os

def add_preconnect(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    preconnects = """
    <link rel="preconnect" href="https://i.postimg.cc" />
    <link rel="preconnect" href="https://api.jsonbin.io" />
    """
    
    if '<link rel="preconnect" href="https://fonts.googleapis.com"' in content:
        content = content.replace('<link rel="preconnect" href="https://fonts.googleapis.com"', preconnects + '\n    <link rel="preconnect" href="https://fonts.googleapis.com"')
        with open(filepath, 'w') as f:
            f.write(content)

add_preconnect('index.html')
add_preconnect('gallery.html')

