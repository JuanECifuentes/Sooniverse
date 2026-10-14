import re
import difflib

# 1. Get original content from git before our changes this session
import subprocess
git_orig = subprocess.check_output(['git', 'show', 'HEAD:apps/core/templates/core/landing.html'], encoding='utf-8')

with open('apps/core/templates/core/landing.html', 'r', encoding='utf-8') as f:
    current = f.read()

def get_texts(html):
    no_script = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    no_style = re.sub(r'<style.*?</style>', '', no_script, flags=re.DOTALL)
    no_django = re.sub(r'\{%.*?%\}|\{\{.*?\}\}', '', no_style, flags=re.DOTALL)
    texts = re.findall(r'>([^<]+)<', no_django)
    return [t.strip() for t in texts if t.strip()]

orig_texts = get_texts(git_orig)
curr_texts = get_texts(current)

print(f"Orig: {len(orig_texts)}, Curr: {len(curr_texts)}")
diff = list(difflib.unified_diff(orig_texts, curr_texts, fromfile='HEAD', tofile='CURRENT', lineterm=''))
if not diff:
    print("SUCCESS: 100% IDENTICAL TEXTS TO HEAD!")
else:
    print("DIFF:")
    for line in diff:
        print(line)
