def main():
    try:
        with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_page.html", "r") as f:
            html = f.read()
            
        print("Printing apply link tag and inner content:")
        idx = html.find("job-apply-resources")
        if idx != -1:
            # Let's find the start of '<a' before this index
            start = html.rfind("<a", 0, idx)
            # Let's find the closing '</a>' after this index
            end = html.find("</a>", idx)
            if start != -1 and end != -1:
                full_tag = html[start:end+4]
                print(full_tag)
                
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
