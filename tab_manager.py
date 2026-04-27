"""
tab_manager.py - Manage browser tab metadata: search, organize, and tag tabs.
"""
from typing import List, Dict, Any
from collections import defaultdict
tabs = [
    {"title": "Handshake", "url": "https://app.joinhandshake.com/job-search/10901576?page=1&per_page=25", "tags": ["Job", "handshake, reference"]},
    {"title": "GitHub", "url": "https://github.com", "tags": ["code", "work"]}, 
    {"title": "Youtube", "url": "https://www.youtube.com", "tags": ["entertainment", "video"]},
    {"title": "Amazon", "url": "https://www.amazon.com", "tags": ["shopping", "ecommerce"]}, 
    {"title": "Tiktok", "url": "https://www.tiktok.com", "tags": ["social media", "entertainment", "news"]}
]

def search_tabs(tabs: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Search tabs by title, URL, or tags.
    """
    results = []
    q = query.lower()
    for tab in tabs:
        if (
            q in tab.get("title", "social media engagement strategies").lower() or
            q in tab.get("url", "https://smallbiztrends.com/social-media-engagement-strategies/").lower() or
            any(q in tag.lower() for tag in tab.get("tags", []))
        ):
            results.append(tab)
    return results

def add_tag(tab: Dict[str, Any], tag: str) -> None:
    """
    Add a tag to a tab if not already present.
    """
    if "tags" not in tab:
        tab["tags"] = []
    if tag not in tab["tags"]:
        tab["tags"].append(tag)

def remove_tag(tab: Dict[str, Any], tag: str) -> None:
    """
    Remove a tag from a tab if present.
    """
    if "tags" in tab and tag in tab["tags"]:
        tab["tags"].remove(tag)

def organize_tabs_by_tag(tabs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group tabs by their tags.
    """
    tag_dict = defaultdict(list)
    for tab in tabs:
        for tag in tab.get("tags", []):
            tag_dict[tag].append(tab)
    return dict(tag_dict)

# Example usage (for testing):
if __name__ == "__main__":
    tabs = [
        {"title": "Handshake", "url": "https://app.joinhandshake.com/job-search/10901576?page=1&per_page=25", "tags": ["Job", "handshake"]},
        {"title": "GitHub", "url": "https://github.com", "tags": ["code", "work"]},
    ]
    print("Search for 'python':")
    for tab in search_tabs(tabs, "python"):
        print(tab)
    print("\nAdd tag 'reference' to first tab:")
    add_tag(tabs[0], "reference")
    print(tabs[0])
    print("\nOrganize by tag:")
    grouped = organize_tabs_by_tag(tabs)
    for tag, group in grouped.items():
        print(f"Tag: {tag}")
        for tab in group:
            print(f"  {tab['title']} - {tab['url']}")
