import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # We want to find the labels that are parents or siblings of QA_12020974, etc.
        # Workable radio fields are often in fieldsets, where the fieldset contains a <legend> or a heading representing the question.
        for qa in ['QA_12020974', 'QA_12020975', 'QA_12020976', 'QA_12020978']:
            element = await page.query_selector(f'input[name="{qa}"]')
            if element:
                # Find the closest fieldset
                fieldset = await page.evaluate('el => {
                    const fs = el.closest("fieldset");
                    if (fs) {
                        // Find any legend or label inside it
                        const legend = fs.querySelector("legend, [data-ui*=\\"legend\\\"], h3");
                        return legend ? legend.textContent.strip() : fs.textContent.strip();
                    }
                    return null;
                }', element)
                print(f'{qa} Fieldset text: {repr(fieldset)}')
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
