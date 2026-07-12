import sys
import json
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome on 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected!")
            contexts = browser.contexts
            print(f"Number of contexts: {len(contexts)}")
            for idx, context in enumerate(contexts):
                print(f"Context {idx}:")
                pages = context.pages
                print(f"  Number of pages: {len(pages)}")
                for p_idx, page in enumerate(pages):
                    try:
                        print(f"    Page {p_idx}: title='{page.title()}', url='{page.url()}'")
                    except Exception as e:
                        print(f"    Page {p_idx}: error: {e}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
