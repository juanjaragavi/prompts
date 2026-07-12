import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        inputs = await page.query_selector_all('input[type="radio"]')
        seen_names = set()
        for inp in inputs:
            name = await inp.get_attribute('name')
            if name and name not in seen_names:
                seen_names.add(name)
                legend_text = await page.evaluate("""el => {
                    const fs = el.closest('fieldset');
                    if (fs) {
                        const legend = fs.querySelector('legend');
                        if (legend) return legend.innerText;
                        const header = fs.querySelector('h2, h3, [role="heading"]');
                        if (header) return header.innerText;
                        // Or maybe there is a div before the radio buttons
                        return fs.innerText.split('\\n')[0];
                    }
                    return null;
                }""", inp)
                print(f"Name: {name}")
                print(f"Legend text: {legend_text}")
                print("-" * 40)
                
        dropdown_label = await page.evaluate("""() => {
            const el = document.querySelector('[name="CA_42077"]');
            if (el) {
                const parent = el.closest('[data-ui="form-field"]');
                if (parent) {
                    const label = parent.querySelector('label');
                    if (label) return label.innerText;
                }
            }
            return null;
        }""")
        print("Dropdown label:", dropdown_label)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
