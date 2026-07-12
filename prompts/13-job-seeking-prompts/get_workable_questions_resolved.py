import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        print("--- Radio Buttons ---")
        radios = await page.query_selector_all('input[type="radio"]')
        seen_names = set()
        for r in radios:
            name = await r.get_attribute('name')
            if name and name not in seen_names:
                seen_names.add(name)
                fieldset = await r.evaluate_handle('el => el.closest("fieldset")')
                if fieldset:
                    # Look for element with id matching aria-labelledby
                    aria_lbl = await fieldset.evaluate('el => el.getAttribute("aria-labelledby")')
                    if aria_lbl:
                        lbl_el = await page.query_selector(f'#{aria_lbl}')
                        if lbl_el:
                            text = await lbl_el.text_content()
                            print(f"{name}: {text.strip()}")
                        else:
                            print(f"{name}: (label element #{aria_lbl} not found)")
                    else:
                        print(f"{name}: (no aria-labelledby)")
                        
        print("\n--- Dropdowns ---")
        # Let's see if there are dropdowns/comboboxes
        comboboxes = await page.query_selector_all('[role="combobox"], select')
        for cb in comboboxes:
            cb_name = await cb.get_attribute('name')
            # Check closest form-field
            parent = await cb.evaluate_handle('el => el.closest("[data-ui*=\'form-field\']")')
            if parent:
                aria_lbl = await parent.evaluate('el => el.getAttribute("aria-labelledby")')
                if aria_lbl:
                    lbl_el = await page.query_selector(f'#{aria_lbl}')
                    if lbl_el:
                        text = await lbl_el.text_content()
                        print(f"{cb_name}: {text.strip()}")
                    else:
                        print(f"{cb_name}: (label element #{aria_lbl} not found)")
                else:
                    # Let's look for label tag inside parent
                    lbl_el = await parent.query_selector('label')
                    if lbl_el:
                        text = await lbl_el.text_content()
                        print(f"{cb_name}: {text.strip()}")
                    else:
                        print(f"{cb_name}: (no label or aria-labelledby)")
            else:
                print(f"Combobox without parent: {cb_name}")
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
