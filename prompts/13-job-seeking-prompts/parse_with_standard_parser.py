import html.parser
import re

class MyHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.links = []
        self.texts = []
        self.in_a = False
        self.current_link = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'a':
            self.in_a = True
            for attr, val in attrs:
                if attr == 'href':
                    self.current_link = val
                    
    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_a = False
            self.current_link = None
            
    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            if self.in_a and self.current_link:
                self.links.append({"text": cleaned, "href": self.current_link})
            self.texts.append(cleaned)

def parse_file(filepath):
    print(f"=== Parsing {filepath} ===")
    with open(filepath, "r") as f:
        parser = MyHTMLParser()
        parser.feed(f.read())
        
        # Look for interesting things
        print("Number of links:", len(parser.links))
        interesting_links = []
        for l in parser.links:
            text_lower = l['text'].lower()
            href_lower = l['href'].lower()
            if "job" in href_lower or "careers" in href_lower or "apply" in href_lower or "role" in href_lower or "position" in href_lower or "vibe" in text_lower or "ai" in text_lower or "developer" in text_lower or "engineer" in text_lower:
                interesting_links.append(l)
                
        print(f"Interesting links ({len(interesting_links)}):")
        # Print unique links to save space
        seen = set()
        count = 0
        for l in interesting_links:
            key = (l['text'], l['href'])
            if key not in seen:
                seen.add(key)
                print(f"  - [{l['text']}]({l['href']})")
                count += 1
                if count >= 40:
                    break
        print("\n" + "="*40 + "\n")

parse_file("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibehackers_io_jobs.html")
parse_file("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/remotevibecodingjobs_com_.html")
parse_file("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibecodecareers_com_.html")
