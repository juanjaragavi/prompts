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
            
            # Print parent's innerHTML or siblings to find labels
            inputs = await page.query_selector_all('input, textarea, select')
            for i, inp in enumerate(inputs):
                name = await inp.get_attribute('name')
                id_ = await inp.get_attribute('id')
                typ = await inp.get_attribute('type')
                
                # Get surrounding text or closest label
                sibling_text = await inp.evaluate("""el => {
                    // Try climbing up up to 3 levels, and find text or label inside the sibling/parent
                    let p = el.parentElement;
                    while (p) {
                        const lbls = p.querySelectorAll('label, .rec-form-label, span');
                        for (let l of lbls) {
                            if (l.textContent.strip) {
                                const txt = l.textContent.trim();
                                if (txt) return txt;
                            } else {
                                const txt = l.innerText ? l.innerText.trim() : '';
                                if (txt) return txt;
                            }
                        }
                        const p_text = p.innerText ? p.innerText.trim() : '';
                        if (p_text && p_text.length < 500) {
                            return p_text.replace(/\n+/g, ' | ');
                        }
                        p = p.parentElement;
                    }
                    return '';
                }""")
                print(f"[{i}] Name: {name}, ID: {id_}, Type: {typ}")
                print(f"    Resolved Context: {repr(sibling_text)}")
                print("-" * 50)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
