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
        
        # Get all label elements on the page
        labels = await page.query_selector_all("label")
        print(f"Found {len(labels)} <label> elements:")
        for idx, lbl in enumerate(labels):
            text = await lbl.text_content()
            for_attr = await lbl.get_attribute("for")
            print(f"  {idx}: for={for_attr} => '{text.strip()}'")
            
        # Get all legend/fieldset/headers elements on the page
        legends = await page.query_selector_all("legend, h3, h4, [data-testid*='question']")
        print(f"\nFound {len(legends)} legend/heading elements:")
        for idx, leg in enumerate(legends):
            text = await leg.text_content()
            tag = await page.evaluate("el => el.tagName", leg)
            print(f"  {idx}: tag={tag} => '{text.strip()}'")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
