from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449", wait_until="load")
        page.wait_for_timeout(5000)
        
        # let's write the outerHTML of the body to a file
        body_html = page.locator("body").evaluate("el => el.outerHTML")
        with open("darwin_body.html", "w") as f:
            f.write(body_html)
        print("Saved body HTML to darwin_body.html")
        page.close()

if __name__ == "__main__":
    main()
