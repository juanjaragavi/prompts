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
        
        # We can find all containers that have QA_ inputs or other form fields
        # Workable often uses [data-testid="form-field"] or [class*="form-field"]
        fields = await page.query_selector_all("[data-testid*='field'], [class*='field']")
        print(f"Found {len(fields)} fields by selector.")
        
        # Alternatively, let's find all custom questions by traversing the parents of QA_ elements
        qa_inputs = await page.query_selector_all("[name*='QA_'], [id*='QA_'], [name*='61442']")
        print(f"Found {len(qa_inputs)} QA or checkbox elements.")
        
        seen_parents = set()
        for idx, inp in enumerate(qa_inputs):
            name = await inp.get_attribute("name")
            id_attr = await inp.get_attribute("id")
            
            # Let's find the ancestor that represents the question container
            # Typically a div with class containing "field" or "section" or "row"
            parent = inp
            for _ in range(5):
                parent = await parent.property("parentNode")
                if not parent:
                    break
                # Check if it has a class or data-testid that makes it a container
                class_name = await parent.to_element_handle().get_attribute("class")
                testid = await parent.to_element_handle().get_attribute("data-testid")
                if (class_name and "field" in class_name.lower()) or (testid and "field" in testid.lower()):
                    break
            
            if parent:
                parent_handle = parent.to_element_handle()
                parent_id = id(parent_handle)
                if parent_id not in seen_parents:
                    seen_parents.add(parent_id)
                    text = await parent_handle.text_content()
                    print(f"\nQuestion field {idx} (name={name}, id={id_attr}):")
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    for l in lines:
                        print(f"  {l}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
