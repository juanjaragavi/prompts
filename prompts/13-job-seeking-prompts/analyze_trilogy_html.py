import re

def main():
    try:
        with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_page.html", "r") as f:
            html = f.read()
            
        # Let's search for "no longer" or "accepting" or similar
        print("Searching for patterns:")
        for pattern in ["no longer", "accepting", "apply", "solicitar", "sencilla", "closed"]:
            matches = list(re.finditer(re.escape(pattern), html, re.IGNORECASE))
            print(f"Pattern '{pattern}': {len(matches)} matches")
            for m in matches[:5]:
                start = max(0, m.start() - 100)
                end = min(len(html), m.end() + 100)
                context = html[start:end]
                # Clean up newlines for printing
                context_clean = context.replace("\n", " ")
                print(f"  Match at {m.start()}: ... {context_clean} ...")
                
        # Let's search for all buttons and check their inner text
        buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.IGNORECASE | re.DOTALL)
        print(f"\nFound {len(buttons)} buttons:")
        for b in buttons:
            clean_b = re.sub(r'<[^>]+>', '', b).strip()
            clean_b = re.sub(r'\s+', ' ', clean_b)
            if clean_b:
                print("Button text:", clean_b)
                
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
