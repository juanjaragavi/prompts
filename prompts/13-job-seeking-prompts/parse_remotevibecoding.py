import re
from bs4 import BeautifulSoup

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    try:
        with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/remotevibecodingjobs_com_.html", "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            print("Title of page:", soup.title.string if soup.title else "N/A")
            
            links = []
            for a in soup.find_all("a", href=True):
                href = a['href']
                text = clean_text(a.get_text())
                links.append({"text": text, "href": href})
                    
            print(f"Found {len(links)} links on the page. Printing:")
            for l in links:
                print(f"- [{l['text']}]({l['href']})")
                
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
