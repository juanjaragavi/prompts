import re
import html

def clean_html(text):
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

files = ['darwin_body.html', 'trilogy_page.html', 'vibeast_content.html']
for fn in files:
    try:
        with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/' + fn, 'r') as f:
            content = f.read()
            print(f"=== File: {fn} ===")
            print("Length:", len(content))
            cleaned = clean_html(content)
            print("Cleaned text snippet (first 1000 chars):")
            print(cleaned[:1000])
            print("\n")
    except Exception as e:
        print(f"Error reading {fn}: {e}")
