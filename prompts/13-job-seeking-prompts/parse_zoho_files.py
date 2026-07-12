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
            await page.wait_for_timeout(5000)
            
            # Print parent structure of file inputs [13], [14], [15], [16]
            file_infos = await page.evaluate("""() => {
                const results = [];
                const inputs = document.querySelectorAll('input[type="file"]');
                inputs.forEach((inp, idx) => {
                    // Let's traverse parents and print parent innerText to see what section it is in
                    let label = '';
                    let parent = inp.parentElement;
                    while (parent) {
                        if (parent.tagName === 'REC-FORM-ROW' || parent.classList.contains('rec-form-row') || parent.classList.contains('rec-form-col')) {
                            label = parent.textContent.trim().replace(/\\s+/g, ' ');
                            break;
                        }
                        parent = parent.parentElement;
                    }
                    results.push({
                        index: idx,
                        name: inp.getAttribute('name'),
                        label: label
                    });
                });
                return results;
            }""")
            
            print("Zoho File Fields:")
            for item in file_infos:
                print(f"Index {item['index']}: name={item['name']}")
                print(f"  Label Context: {repr(item['label'])}")
                print("-" * 50)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
