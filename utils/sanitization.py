import re

def sanitize_input(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)
