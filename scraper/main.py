import requests
from bs4 import BeautifulSoup
import json
import re

# 1. Fetch the raw markdown
RAW_MD_URL = (
    "https://raw.githubusercontent.com/"
    "HighwayofLife/awesome-chatgpt-plugins/master/README.md"
)
resp = requests.get(RAW_MD_URL)
resp.raise_for_status()
md = resp.text

# 2. Convert to HTML
from markdown import markdown
html = markdown(md)

# 3. Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
data = []

# 4. Find the "Categories" heading
heading = soup.find("h2", string=lambda s: s and "Categories" in s)
if not heading:
    print("❌ Couldn't find Categories heading")
    exit(1)

# 5. Grab the next <ul> and pull each <li>
ul = heading.find_next_sibling("ul")
for li in ul.find_all("li"):
    text = li.get_text(strip=True)  # e.g. "Charts and Diagrams – 26 plugins"
    # split on the dash and extract count
    parts = re.split(r"\s*[-–—]\s*", text, maxsplit=1)
    if len(parts) == 2 and (m := re.search(r"(\d+)", parts[1])):
        data.append({
            "category": parts[0],
            "count": int(m.group(1))
        })

# 6. Save to JSON
with open("scraper/raw_tools.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✅ Scraped {len(data)} categories")