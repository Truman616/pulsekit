import requests
import json
import time
from datetime import datetime, timezone

# Broad search queries to fetch recent posts
QUERIES = [
    "automate",
    "scraper",
    "scraping",
    "python script",
    "api wrapper"
]

# Expanded list of relevant subreddits where people ask for automation/scrapers
TARGET_SUBREDDITS = {
    # Automation & Tech
    "automation", "webscraping", "dataengineering", "python", "learnpython", "nocode", 
    "zapier", "makecom", "shortcuts", "powershell", "datascience",
    # Marketing, Sales & Growth
    "GrowthHacking", "marketing", "digitalmarketing", "sales", "leadgeneration", "coldemail", "seo",
    # Business, Startups & Projects
    "smallbusiness", "startup", "entrepreneur", "saas", "solopreneur", "sideproject", "eCommerce", "shopify",
    # Freelance & Hiring
    "forhire", "Freelance_Assistant", "freelance", "jobs"
}

# Intent keywords that suggest someone is looking for help, a tool, or a script
INTENT_KEYWORDS = [
    "how", "help", "need", "hire", "looking for", "is there", "can someone", 
    "recommend", "suggest", "advice", "problem", "issue", "trying to", "want to",
    "automatic", "automatically", "tool", "software", "api", "cron", "run"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def has_lead_intent(title, text):
    content = (title + " " + text).lower()
    return any(keyword in content for keyword in INTENT_KEYWORDS)

def fetch_leads():
    leads = []
    seen_ids = set()
    
    print("[*] Scanning Reddit for active automation leads...")
    
    for query in QUERIES:
        # Search sorting by 'new' to get the latest posts
        url = f"https://www.reddit.com/search.json?q={requests.utils.quote(query)}&sort=new&limit=100"
        headers = {"User-Agent": USER_AGENT}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[!] Failed to fetch query '{query}': HTTP {response.status_code}")
                continue
                
            data = response.json()
            posts = data.get("data", {}).get("children", [])
            
            for post in posts:
                post_data = post.get("data", {})
                post_id = post_data.get("id")
                
                if post_id in seen_ids:
                    continue
                    
                seen_ids.add(post_id)
                
                # Check subreddit relevance
                sub = post_data.get("subreddit", "")
                if sub.lower() not in [s.lower() for s in TARGET_SUBREDDITS]:
                    continue
                
                # Filter out posts that don't look like questions or requests for help
                title = post_data.get("title", "")
                text = post_data.get("selftext", "")
                if not has_lead_intent(title, text):
                    continue
                    
                created_utc = post_data.get("created_utc")
                if not created_utc:
                    continue
                    
                post_time = datetime.fromtimestamp(created_utc, timezone.utc)
                now = datetime.now(timezone.utc)
                age_days = (now - post_time).total_seconds() / 86400.0
                
                # Filter posts older than 7 days
                if age_days > 7:
                    continue
                    
                leads.append({
                    "title": title,
                    "subreddit": sub,
                    "author": post_data.get("author"),
                    "url": f"https://www.reddit.com{post_data.get('permalink')}",
                    "text": text,
                    "age_days": age_days,
                    "created": post_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                })
                
            # Pause to respect rate limits
            time.sleep(1.5)
            
        except Exception as e:
            print(f"[x] Error during query '{query}': {e}")
            
    # Sort leads by age (newest first)
    leads.sort(key=lambda x: x["age_days"])
    return leads

def save_leads_markdown(leads):
    filename = "leads.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# ⚡ Live Reddit Automation Leads\n\n")
        f.write(f"*Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        
        if not leads:
            f.write("No active leads found in the past 7 days. Try running the script again later.\n")
            return
            
        f.write(f"Found **{len(leads)}** active threads from the past 7 days.\n\n")
        f.write("---\n\n")
        
        for idx, lead in enumerate(leads, 1):
            f.write(f"### {idx}. [{lead['title']}]({lead['url']})\n")
            f.write(f"- **Subreddit**: r/{lead['subreddit']}\n")
            f.write(f"- **Author**: u/{lead['author']}\n")
            f.write(f"- **Created**: {lead['created']} ({lead['age_days']:.1f} days ago)\n\n")
            
            snippet = lead['text'][:300] + "..." if len(lead['text']) > 300 else lead['text']
            if snippet.strip():
                f.write(f"> {snippet.strip().replace('\n', '\n> ')}\n\n")
            else:
                f.write("> *(No description text)*\n\n")
                
            f.write("---\n\n")
            
    print(f"[+] Saved {len(leads)} leads to {filename}")

if __name__ == "__main__":
    leads = fetch_leads()
    save_leads_markdown(leads)
