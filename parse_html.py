import re

def parse():
    try:
        with open('inspect_ps5_search.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        print(f"File size: {len(html)} bytes")
        
        # Check for "Sugestões"
        if "Sugestões" in html:
            print("Text 'Sugestões' found in HTML!")
            # Print context
            idx = html.find("Sugestões")
            print(f"Context: {html[idx-100:idx+200]}")
        else:
            print("Text 'Sugestões' NOT found in HTML.")
            
        # Find links with class containing "cat" or "sug"
        # <a ... class="...cat..." ...>
        
        # Regex for <a> tags
        link_pattern = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)
        
        matches = link_pattern.findall(html)
        print(f"Total links found: {len(matches)}")
        
        for href, text in matches:
            text = text.strip()
            # Remove tags from text
            text = re.sub(r'<[^>]+>', '', text).strip()
            
            if not text: continue
            
            if 'cat' in href or 'sug' in href:
                 print(f"  Potential Match: {text} -> {href}")
                 
            if text.lower() in ['consoles', 'games', 'jogos', 'acessórios', 'videogames', 'sony']:
                 print(f"  [KEYWORD MATCH] {text} -> {href}")

        # Look for the specific structure the user might be referring to
        # <div class="hidden-xs ctg-suggestions">
        if "ctg-suggestions" in html:
            print("Found 'ctg-suggestions' class!")
        else:
            print("'ctg-suggestions' class NOT found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse()
