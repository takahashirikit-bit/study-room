import json
import yaml
import os

def update_template():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    books_path = os.path.join(base_dir, "00_meta", "books.json")
    template_path = os.path.join(base_dir, ".github", "ISSUE_TEMPLATE", "study_log.yaml")

    with open(books_path, "r", encoding="utf-8") as f:
        books = json.load(f)
    book_titles = [b["title"] for b in books]
    print(f"Loaded books: {book_titles}")

    with open(template_path, "r", encoding="utf-8") as f:
        template = yaml.safe_load(f)

    found = False
    for item in template.get("body", []):
        if item.get("id") == "book_title":
            item["attributes"]["options"] = book_titles
            found = True
    
    if not found:
        print("Error: 'book_title' id not found in template.")
        return

    with open(template_path, "w", encoding="utf-8") as f:
        yaml.dump(template, f, allow_unicode=True, sort_keys=False)
    
    print("Successfully updated the template.")

if __name__ == "__main__":
    update_template()
