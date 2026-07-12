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
        
        # Find the dropdown input and click it to open the list
        dropdown_input = await page.query_selector("#input_QA_11736014_input")
        if dropdown_input:
            print("Found dropdown input! Clicking it to open options...")
            
            # Find the label or section title right before or above it
            parent_text = await page.evaluate("""(el) => {
                let parent = el.parentElement;
                while (parent) {
                    if (parent.textContent && parent.textContent.includes('?')) {
                        return parent.textContent;
                    }
                    parent = parent.parentElement;
                }
                return null;
            }""", dropdown_input)
            print(f"Parent context of dropdown: {parent_text.strip() if parent_text else None}")
            
            # Click the dropdown to show options
            await dropdown_input.click()
            await page.wait_for_timeout(1000)
            
            # Workable dropdown options are usually loaded in an active list/menu
            # Let's search for listbox, option, or items with role="option"
            options = await page.query_selector_all("[role='option'], [class*='option'], li[id*='option']")
            print(f"Found {len(options)} options in active dropdown menu:")
            for idx, opt in enumerate(options):
                opt_text = await opt.text_content()
                opt_id = await opt.get_attribute("id")
                print(f"  {idx}: id={opt_id} => '{opt_text.strip()}'")
        else:
            print("Dropdown input not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
