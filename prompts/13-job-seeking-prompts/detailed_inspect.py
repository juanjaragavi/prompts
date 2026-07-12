import sys
import json
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome on 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            pages = context.pages
            print(f"Found {len(pages)} pages")
            
            results = []
            for idx, page in enumerate(pages):
                try:
                    title = page.title()
                    url = page.url()
                    
                    # Skip non-http/https urls or search engines
                    if not url.startswith("http"):
                        continue
                    if "google.com/search" in url or "duckduckgo.com" in url:
                        continue
                        
                    # Let's inspect the page elements to see if it's an application form
                    # We look for inputs: name, email, file (resume)
                    # and see if it's an apply page.
                    inputs = page.locator("input").count()
                    file_inputs = page.locator("input[type='file']").count()
                    textareas = page.locator("textarea").count()
                    
                    # We can also check some text in the page
                    body_text = ""
                    try:
                        body_text = page.locator("body").inner_text()
                    except Exception:
                        pass
                        
                    has_form = False
                    # Heuristics for unfilled job application form:
                    # Usually contains file input (for resume) or multiple text/email inputs, 
                    # and URL often contains "apply", "application", "jobs", "job", "career", etc.
                    # Let's log them to inspect manually first.
                    results.append({
                        "index": idx,
                        "title": title,
                        "url": url,
                        "inputs": inputs,
                        "file_inputs": file_inputs,
                        "textareas": textareas,
                        "body_length": len(body_text),
                        "snippet": body_text[:200].replace("\n", " ") if body_text else ""
                    })
                except Exception as e:
                    print(f"Error inspecting page {idx}: {e}")
                    
            print(json.dumps(results, indent=2))
            with open("detailed_inspect.json", "w") as f:
                json.dump(results, f, indent=2)
                
        except Exception as e:
            print("Error connecting/running:", e)

if __name__ == "__main__":
    main()
