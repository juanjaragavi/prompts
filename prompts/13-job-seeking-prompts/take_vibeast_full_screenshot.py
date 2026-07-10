import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Find the Vibeast LinkedIn job page
            vibeast_page = None
            for page in context.pages:
                url = page.url
                if "vibeast-4401002722" in url:
                    vibeast_page = page
                    break
            
            if not vibeast_page:
                print("Vibeast LinkedIn job page not found.")
                return
            
            print(f"Using Vibeast page: {vibeast_page.title()} | {vibeast_page.url}")
            vibeast_page.bring_to_front()
            vibeast_page.wait_for_timeout(3000)
            
            # Take a full page screenshot
            proof_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibeast_closed_proof.png"
            vibeast_page.screenshot(path=proof_path, full_page=False)
            print(f"Proof screenshot saved to {proof_path}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
