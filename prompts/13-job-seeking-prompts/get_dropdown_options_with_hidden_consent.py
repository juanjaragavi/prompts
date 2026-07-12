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
        
        # Hide cookie consent and backdrops
        await page.evaluate("""() => {
            const consent = document.querySelector('[data-ui="cookie-consent"]');
            if (consent) consent.style.removeProperty ? consent.remove() : consent.style.display = 'none';
            
            const backdrops = document.querySelectorAll('[data-ui="backdrop"]');
            for (let b of backdrops) b.remove ? b.remove() : b.style.display = 'none';
            
            // Also enable pointer events on everything if restricted
            document.body.style.pointerEvents = 'auto';
        }""")
        
        print("Hiding consent banner done.")
        
        # Find the dropdown input and click it
        dropdown_input = await page.query_selector("#input_QA_11736014_input")
        if dropdown_input:
            print("Found dropdown input! Clicking it...")
            await dropdown_input.click()
            await page.wait_for_timeout(1000)
            
            # Find list options
            options = await page.query_selector_all("[role='option'], li[id*='option']")
            print(f"Found {len(options)} options in dropdown:")
            for idx, opt in enumerate(options):
                opt_text = await opt.text_content()
                opt_id = await opt.get_attribute("id")
                print(f"  {idx}: id={opt_id} => '{opt_text.strip()}'")
        else:
            print("Dropdown input not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
