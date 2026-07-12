import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Bypassing cookies
        await page.evaluate("""() => {
            const consent = document.querySelector('[data-ui="cookie-consent"]');
            if (consent) consent.remove();
        }""")
        
        # Let's inspect the page inputs and sections
        form = await page.query_selector('form')
        if not form:
            print("Form not found!")
            return
            
        elements = await page.evaluate("""() => {
            const list = [];
            const els = document.querySelectorAll('input, textarea, select, label, h2, h1');
            for (let el of els) {
                list.push({
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    name: el.getAttribute('name'),
                    id: el.getAttribute('id'),
                    placeholder: el.getAttribute('placeholder'),
                    text: el.textContent ? el.textContent.trim() : '',
                    html: el.outerHTML.substring(0, 200)
                });
            }
            return list;
        }""")
        
        print(f"Found {len(elements)} elements:")
        for idx, el in enumerate(elements):
            if el['tag'] in ['LABEL', 'H2', 'H1']:
                print(f"[{idx}] {el['tag']}: {repr(el['text'])}")
            else:
                print(f"[{idx}] {el['tag']} ({el['type']}): name={el['name']}, id={el['id']}, placeholder={el['placeholder']}")
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
