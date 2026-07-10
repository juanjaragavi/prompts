import json

def filter_non_matched():
    with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/extracted_bogota_jobs.md', 'r') as f:
        text = f.read()

    # Strip markdown code blocks if present
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0]
    elif '```' in text:
        text = text.split('```')[1].split('```')[0]

    jobs = json.loads(text.strip())

    titles = ['artificial intelligence engineer', 'ai engineer', 'ai developer', 'generative ai developer', 'prompt engineer', 'machine learning engineer']

    non_matched_jobs = []
    for j in jobs:
        title_lower = j['title'].lower()
        matched = False
        for t in titles:
            if t in title_lower:
                matched = True
                break
        if 'ingeniero' in title_lower and ('inteligencia artificial' in title_lower or 'machine learning' in title_lower or 'ia' in title_lower or 'aprendizaje' in title_lower):
            matched = True
        if not matched:
            non_matched_jobs.append(j)

    print(f"Total non-matched: {len(non_matched_jobs)}")
    for j in non_matched_jobs:
        loc = j['location'].replace('\n', ' ')
        print(f"### {j['title']} at {j['company']}")
        print(f"- **Link:** {j['link']}")
        print(f"- **Location/Details:** {loc}")
        print(f"- **Reason for Exclusion:** Does not match the permitted target job titles or is a generic/unrelated role.")
        print()

if __name__ == '__main__':
    filter_non_matched()
