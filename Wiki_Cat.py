import wikipediaapi

# Initialize the Wikipedia API
wiki = wikipediaapi.Wikipedia(user_agent='Six Degrees of Wikipedia', language='en')

def gather_articles(category, max_depth=1, current_depth=0):
    """
    Recursively gather all articles from a category and its subcategories
    max_depth = 1 will include subcategories of the category
    max_depth = 2 will inlude subcategories of the subcategories
    """
    articles = []
    
    # Loop through all members of the category
    for member in category.categorymembers.values():
        # If it's a category and we haven't reached max depth, recurse into it
        if member.ns == wikipediaapi.Namespace.CATEGORY and current_depth < max_depth:
            articles += gather_articles(member, max_depth, current_depth + 1)
        # If it's an article, add it to the list
        elif member.ns == wikipediaapi.Namespace.MAIN:
            articles.append(member.title)
    
    return articles

# Get the category page
catE = wiki.page("Category:Entertainment")
catP = wiki.page("Category:Politics")

# Gather articles from entertainment category and its subcategories (depth 2)
ent_articles = gather_articles(catE, max_depth=2)
pol_articles = gather_articles(catP, max_depth=1)

all_articles = set(ent_articles + pol_articles)

print(f"Found {len(all_articles)} articles in '{catE.title}' (depth 2) and '{catP.title}' (depth 1).")

# Save article titles to a file, one per line
with open("article_titles.txt", "w", encoding="utf-8") as f:
    for title in all_articles:
        f.write(title + "\n")