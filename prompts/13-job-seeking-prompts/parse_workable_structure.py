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
        
        # In Workable, sections of the form have data-testid or custom tags.
        # Let's find all divs containing class "form-field" or having similar class or role
        containers = await page.query_selector_all("div[class*='form-field'], div[class*='question'], fieldset, div[role='group']")
        print(f"Found {len(containers)} question containers:\n")
        
        for idx, container in enumerate(containers):
            # Let's see if the container contains input elements
            inputs = await container.query_selector_all("input, textarea, select")
            if not inputs:
                continue
                
            # Get the text content of the container but remove child input texts to get the question/label text
            full_text = await container.text_content()
            clean_lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            print(f"--- Container {idx} ---")
            print("Text content lines:")
            for line in clean_lines[:10]:
                print(f"  {line}")
            if len(clean_lines) > 10:
                print(f"  ... ({len(clean_lines)-10} more lines)")
                
            print("Inputs inside this container:")
            for inp in inputs:
                tag = await page.evaluate("el => el.tagName", inp)
                typ = await inp.get_attribute("type")
                name = await inp.get_attribute("name")
                id_attr = await inp.get_attribute("id")
                value = await inp.get_attribute("value")
                # Try to find text of its parent label if it exists
                parent_text = ""
                parent = await page.evaluate_handle("el => el.parentElement", inp)
                if parent:
                    parent_text = await parent.evaluate("el => el.textContent")
                print(f"  - tag={tag}, type={typ}, name={name}, id={id_attr}, value={value}, parent_text={parent_text.strip() if parent_text else None}")
            print()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
