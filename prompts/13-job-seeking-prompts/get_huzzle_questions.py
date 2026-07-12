import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = "https://apply.workable.com/huzzle/j/C51C2BFA00/apply/"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Let's find all question sections
        # Workable often uses sections with data-testid or custom class names,
        # or simple form sections. Let's find all labels or spans or divs with text.
        # Let's query form-row or sections.
        sections = await page.query_selector_all("main form > div, main form fieldset")
        print(f"Found {len(sections)} form sections:")
        
        for i, sec in enumerate(sections):
            text = await sec.text_content()
            # Let's only print sections with brief context to avoid overflow
            # We can print clean text lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            print(f"\n--- Section {i} ---")
            for line in lines[:15]: # Show first 15 non-empty lines
                print(f"  {line}")
            if len(lines) > 15:
                print(f"  ... ({len(lines)-15} more lines)")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
