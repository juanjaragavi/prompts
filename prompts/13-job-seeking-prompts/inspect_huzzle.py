import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a realistic user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = "https://apply.workable.com/huzzle/j/C51C2BFA00/apply/"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception as e:
            print(f"Navigation warning/error: {e}")
            
        print("Waiting 5 seconds for page to load fully...")
        await page.wait_for_timeout(5000)
        
        # Take a screenshot
        screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/huzzle_inspect.png"
        await page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Get page title and some text
        title = await page.title()
        print(f"Page title: {title}")
        
        # Dump input elements
        inputs = await page.query_selector_all("input, textarea, select")
        print(f"Found {len(inputs)} input/textarea/select elements:")
        for idx, inp in enumerate(inputs):
            name = await inp.get_attribute("name")
            id_attr = await inp.get_attribute("id")
            placeholder = await inp.get_attribute("placeholder")
            type_attr = await inp.get_attribute("type")
            label = ""
            # Try to find associated label
            if id_attr:
                label_el = await page.query_selector(f"label[for='{id_attr}']")
                if label_el:
                    label = await label_el.text_content()
            
            # Print tagName via evaluate
            tag_name = await page.evaluate("el => el.tagName", inp)
            print(f"{idx}: tag={tag_name}, type={type_attr}, name={name}, id={id_attr}, label={label.strip() if label else None}, placeholder={placeholder}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
