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
            
            # Now let's execute JS to map each input to its text label cleanly
            mapping = await page.evaluate("""() => {
                const results = [];
                const inputs = document.querySelectorAll('input, textarea, select');
                inputs.forEach((inp, idx) => {
                    let labelText = '';
                    
                    // Try climbing up to find any preceding label or sibling text
                    let p = inp.parentElement;
                    while (p) {
                        const label = p.querySelector('label, .rec-form-label, span');
                        if (label && label.textContent.trim()) {
                            labelText = label.textContent.trim();
                            break;
                        }
                        p = p.parentElement;
                    }
                    
                    if (!labelText) {
                        // Just get the placeholder
                        labelText = inp.getAttribute('placeholder') || '';
                    }
                    
                    results.push({
                        index: idx,
                        name: inp.getAttribute('name'),
                        id: inp.getAttribute('id'),
                        type: inp.getAttribute('type'),
                        tag: inp.tagName,
                        label: labelText.replace(/\\s+/g, ' ')
                    });
                });
                return results;
            }""")
            
            print(f"Mapped {len(mapping)} inputs:")
            for item in mapping:
                print(f"[{item['index']}] Name: {item['name']}, ID: {item['id']}, Type: {item['type']}, Tag: {item['tag']}")
                print(f"    Label: {repr(item['label'])}")
                print("-" * 50)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
