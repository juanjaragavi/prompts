import sys
import json
import time
from playwright.sync_api import sync_playwright

def search_ddg(page, query):
    print(f"Searching DuckDuckGo for: {query}...")
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    page.goto(url, wait_until="load")
    page.wait_for_timeout(3000)
    
    # Extract links and snippets
    links = []
    results = page.query_selector_all(".result__results .result")
    for r in results:
        title_elem = r.query_selector(".result__title a")
        snippet_elem = r.query_selector(".result__snippet")
        if title_elem:
            title = title_elem.inner_text().strip()
            href = title_elem.get_attribute("href")
            snippet = snippet_elem.inner_text().strip() if snippet_elem else ""
            links.append({"title": title, "url": href, "snippet": snippet})
    return links

import urllib.parse

def main():
    print("Connecting to Chrome on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.new_page()
            
            queries = [
                'site:ycombinator.com/jobs "AI" OR "LLM" OR "Cursor" OR "AI agent"',
                'site:wellfound.com/jobs "AI"',
                '"vibe coding" job OR "vibe coder" job',
                '"AI-assisted software development" job',
                '"LLM-augmented development" job'
            ]
            
            all_links = {}
            for q in queries:
                links = search_ddg(page, q)
                print(f"Found {len(links)} results for query '{q}'")
                for link in links:
                    url = link["url"]
                    if url not in all_links:
                        all_links[url] = link
                        
            # Save results
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/discovered_ddg_links.json", "w") as f:
                json.dump(list(all_links.values()), f, indent=2)
            print(f"Saved {len(all_links)} unique links to discovered_ddg_links.json")
            
            page.close()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
