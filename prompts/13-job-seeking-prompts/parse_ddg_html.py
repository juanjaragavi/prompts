from playwright.sync_api import sync_playwright
import json

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        # Load local HTML to parse it in browser context
        page.goto("file:///Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/simple_search_ddg.html")
        
        results = []
        result_divs = page.query_selector_all(".result__results .result")
        print("Number of results found in container:", len(result_divs))
        
        # If .result__results is not found, let's look for general links in result class
        if len(result_divs) == 0:
            result_divs = page.query_selector_all(".result")
            print("Number of .result items:", len(result_divs))
            
        for r in result_divs:
            title_elem = r.query_selector(".result__title a")
            snippet_elem = r.query_selector(".result__snippet")
            if title_elem:
                title = title_elem.inner_text().strip()
                href = title_elem.get_attribute("href")
                snippet = snippet_elem.inner_text().strip() if snippet_elem else ""
                results.append({"title": title, "url": href, "snippet": snippet})
                
        print(json.dumps(results, indent=2))
        page.close()

if __name__ == "__main__":
    main()
