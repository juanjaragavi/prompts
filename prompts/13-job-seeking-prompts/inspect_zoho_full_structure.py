import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://workbetternow.zohorecruit.com/jobs/Careers/746650000037462674/AI-Software-Developer-Internal-Tools', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        apply_btn = await page.query_selector("button:has-text('Apply'), a:has-text('Apply'), [id*='apply']")
        if apply_btn:
            await apply_btn.click()
            await page.wait_for_timeout(4000)
            
            # Print elements
            els_info = await page.evaluate("""() => {
                const list = [];
                const rows = document.querySelectorAll('rec-form-row, .rec-form-row, .rec-form-col');
                for (let r of rows) {
                    const inputs = r.querySelectorAll('input, textarea, select');
                    const label = r.querySelector('label, .rec-form-label, span');
                    list.push({
                        text: r.textContent.trim().replace(/\s+/g, ' '),
                        inputs: Array.from(inputs).map(inp => ({
                            name: inp.getAttribute('name'),
                            id: inp.getAttribute('id'),
                            type: inp.getAttribute('type'),
                            tag: inp.tagName
                        }))
                    });
                }
                return list;
            }""")
            
            print(f"Found {len(els_info)} Zoho form rows:")
            for idx, item in enumerate(els_info):
                print(f"Row {idx}:")
                print(f"  Text content: {repr(item['text'][:300])}")
                print(f"  Inputs: {item['inputs']}")
                print("-" * 50)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
