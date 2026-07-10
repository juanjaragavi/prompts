import json

with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/extracted_bogota_jobs.md', 'r') as f:
    text = f.read()

# Strip markdown code blocks if present
if '```json' in text:
    text = text.split('```json')[1].split('```')[0]
elif '```' in text:
    text = text.split('```')[1].split('```')[0]

jobs = json.loads(text.strip())

titles = ['artificial intelligence engineer', 'ai engineer', 'ai developer', 'generative ai developer', 'prompt engineer', 'machine learning engineer']

matched_jobs = []
for j in jobs:
    title_lower = j['title'].lower()
    matched = False
    for t in titles:
        if t in title_lower:
            matched = True
            break
    if 'ingeniero' in title_lower and ('inteligencia artificial' in title_lower or 'machine learning' in title_lower or 'ia' in title_lower or 'aprendizaje' in title_lower):
        matched = True
    if matched:
        matched_jobs.append(j)

print(json.dumps(matched_jobs, indent=2))
