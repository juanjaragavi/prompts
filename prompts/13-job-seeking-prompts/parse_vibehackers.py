import re
from bs4 import BeautifulSoup

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    try:
        with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibehackers_io_jobs.html", "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            
            # Find all job items. Let's see how they are structured.
            # In vibehackers, we had text:
            # "AI/ML Computational Science Sr Analyst\nAccenture\n•\n⭐\n3.9\n(28686)\n•\n👥\n10k+\n•\nSoftware Engineering\nMentions vibe-coding and AI-assisted tools (GitHub Copilot, Kiro) and expects familiarity with LLMs, LangChain and prompt engineering."
            # Let's inspect the tags.
            print("Title of page:", soup.title.string if soup.title else "N/A")
            
            # Print some raw HTML around the "AI/ML Computational Science" text to find the structure
            body_text = soup.get_text()
            print("Total text length:", len(body_text))
            
            # Search for links containing "jobs" or external portals
            links = []
            for a in soup.find_all("a", href=True):
                href = a['href']
                text = clean_text(a.get_text())
                if "jobs" in href or "careers" in href or "apply" in href or len(text) > 10:
                    links.append({"text": text, "href": href})
                    
            print(f"Found {len(links)} links on the page. Printing first 30:")
            for l in links[:30]:
                print(f"- [{l['text']}]({l['href']})")
                
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
