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
        
        # Let's evaluate in browser to traverse the DOM in-order and output text for inputs and labels
        script = """() => {
            let results = [];
            let elements = document.querySelectorAll('form *');
            for (let el of elements) {
                // Let's only look at headers, labels, legends, or form fields themselves
                let tag = el.tagName;
                if (['H1', 'H2', 'H3', 'H4', 'LEGEND', 'LABEL', 'INPUT', 'TEXTAREA', 'SELECT'].includes(tag)) {
                    // Avoid duplicating nested elements text
                    let text = '';
                    if (['H1', 'H2', 'H3', 'H4', 'LEGEND', 'LABEL'].includes(tag)) {
                        // Get direct text or text content
                        text = el.innerText || el.textContent;
                        text = text.trim();
                        // Skip if empty or duplicates a parent/child too much
                        if (!text) continue;
                    }
                    
                    let item = {
                        tag: tag,
                        text: text
                    };
                    
                    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag)) {
                        item.type = el.getAttribute('type');
                        item.name = el.getAttribute('name');
                        item.id = el.getAttribute('id');
                        item.value = el.getAttribute('value');
                        item.placeholder = el.getAttribute('placeholder');
                    }
                    
                    // Only add if not identical to last added text
                    if (results.length > 0 && results[results.length - 1].tag === tag && results[results.length - 1].text === text && text !== '') {
                        continue;
                    }
                    results.push(item);
                }
            }
            return results;
        }"""
        
        items = await page.evaluate(script)
        print(f"Traversed {len(items)} elements in form:")
        for idx, item in enumerate(items):
            if item['tag'] in ['INPUT', 'TEXTAREA', 'SELECT']:
                print(f"  [{idx}] INPUT: tag={item['tag']}, type={item.get('type')}, name={item.get('name')}, id={item.get('id')}, placeholder={item.get('placeholder')}, value={item.get('value')}")
            else:
                # print text but limit size
                text_short = item['text'].replace('\n', ' ')[:100]
                print(f"  [{idx}] TEXT ({item['tag']}): '{text_short}'")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
