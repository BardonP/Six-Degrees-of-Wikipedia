from bs4 import BeautifulSoup
import re

test_set = "subset_final.xml"
output = "article_links.csv"

#Open the XML file and parse it using BeautifulSoup
with open(test_set, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "xml")

# Find all "page" elements in the XML
pages = soup.find_all("page")

# Extract article titles from the pages
titles = set(page.find("title").text for page in pages)

# Create a dictionary to store article titles and their corresponding links
article_links = {}

# Loop through each page and extract the title and text
for page in pages:
    title = page.find("title").text
    text = page.find("text").text
    
    # Find all hyperlinks in the text
    hyperlinks = re.findall(r'\[\[(.*?)\]\]', text)

    # List of clean links after processing
    clean_links = []
    # List of prefixes to skip
    skip_prefixes = ["File:", "Category:","Template:", "Help:", "Wikipedia:"]

    for link in hyperlinks:
        # Remove display text
        link = link.split("|")[0]

        # Remove section references
        link = link.split("#")[0]
            
        #Skip links with certain prefixes
        if any(link.startswith(prefix) for prefix in skip_prefixes):
            continue

        # Only add the link if it is in the set of article titles
        if link in titles:
            clean_links.append(link)            

    # Store the clean links in the dictionary with the article title as the key
    article_links[title] = clean_links

# Print results
for title, links in article_links.items():
    print(f"Article: {title}")
    print("Links:")
    for link in links:
        print(f" - {link}")
    print(len(links))

# Print total links
total_links = sum(len(links) for links in article_links.values())
print(f"Total links found: {total_links}")

# Save article dictionary (aka edge list) to a CSV
with open(output, "w", encoding="utf-8") as file:
    for title, links in article_links.items():
        file.write(f"{title},{','.join(links)}\n")