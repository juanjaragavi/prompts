import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://ats.rippling.com/curve-dental/jobs/ef73da8e-d943-4bd0-9921-415901a748aa/apply?jobBoardSlug=curve-dental&jobId=ef73da8e-d943-4bd0-9921-415901a748aa&step=application', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Now let's execute JS to map each input to its text label cleanly
        mapping = await page.evaluate("""() => {
            const results = [];
            const inputs = document.querySelectorAll('input, textarea, select, div[role="combobox"]');
            inputs.forEach((inp) => {
                let labelText = '';
                // Try to find any preceding text or closest label
                let parent = inp.parentElement;
                while (parent) {
                    const label = parent.querySelector('label, [class*="label"], span');
                    if (label && label.textContent.trim()) {
                        labelText = label.textContent.trim();
                        break;
                    }
                    parent = parent.parentElement;
                }
                results.push({
                    name: inp.getAttribute('name'),
                    id: inp.getAttribute('id'),
                    type: inp.getAttribute('type'),
                    tag: inp.tagName,
                    label: labelText.replace(/\\s+/g, ' ')
                });
            });
            return results;
        }""")
        
        print("Rippling Fields Mapping:")
        for item in mapping:
            print(f"ID: {item['id']}, Name: {item['name']}, Type: {item['type']}, Tag: {item['tag']}")
            print(f"  Label: {repr(item['label'])}")
            print("-" * 50)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
