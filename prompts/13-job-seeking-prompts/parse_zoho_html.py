from bs4 import BeautifulSoup

with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/zoho_form.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

inputs = soup.find_all(['input', 'textarea', 'select'])
print(f"Total inputs found: {len(inputs)}")

for idx, inp in enumerate(inputs):
    name = inp.get('name')
    id_ = inp.get('id')
    typ = inp.get('type')
    placeholder = inp.get('placeholder')
    
    # Try to find associated label or text
    # In Zoho Recruit, often we have a container div like .rec-form-row or similar
    row = inp.find_parent(class_=['rec-form-row', 'form-group', 'rec-form-col'])
    if row:
        row_text = ' '.join(row.stripped_strings)
        print(f"[{idx}] Name: {name}, ID: {id_}, Type: {typ}, Placeholder: {placeholder}")
        print(f"    Parent row text: {repr(row_text[:200])}")
    else:
        # Just search general parents
        parent = inp.parent
        print(f"[{idx}] Name: {name}, ID: {id_}, Type: {typ}, Placeholder: {placeholder}")
        print(f"    Parent tag text: {repr(' '.join(parent.stripped_strings)[:200])}")
    print("-" * 50)
