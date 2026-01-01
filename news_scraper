import requests
import tldextract
import re
import time
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (DomainHarvester)"}
ALL_DOMAINS = set()
VISITED_URLS = set()
MAX_DEPTH = 3  # recursion depth

ALLOWED_TLDS = (
    ".co.uk", ".org.uk", ".gov.uk", ".ac.uk",
    ".com", ".org", ".net", ".us",
    ".ca", ".com.au", ".net.au", ".org.au",
    ".ie", ".nz"
)

EXCLUDE_DOMAINS = [
    "wikipedia.org",
    "techradar.com",
    "engadget.com",
    "borninspace.com",
    "ign.com",
    "gamespot.com",
    "kotaku.com",
    "pcgamer.com",
    "eurogamer.net"
]

def clean_domain(domain):
    for p in ("www.", "m.", "amp."):
        if domain.startswith(p):
            domain = domain[len(p):]
    return domain

def extract_domain(url):
    try:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return clean_domain(f"{ext.domain}.{ext.suffix}")
    except:
        pass
    return None

def is_english_domain_or_news(url):
    d = extract_domain(url)
    # Allow if in allowed TLDs or contains "news" anywhere in the URL
    return (d and d.endswith(ALLOWED_TLDS)) or ("news" in url.lower())

def add_domain_from_url(url):
    if not url:
        return
    if any(exc in url for exc in EXCLUDE_DOMAINS):
        return
    if not is_english_domain_or_news(url):
        return
    d = extract_domain(url)
    if not d:
        return
    # Add uBlock wildcard format
    rule = f"||{d}^"
    if rule not in ALL_DOMAINS:
        ALL_DOMAINS.add(rule)
        print(f"✔ Added: {rule}")
    # Also check if "news" appears anywhere in the URL (subdomain or path)
    if "news" in url.lower() and d:
        wildcard_rule = f"||*.{d}^"
        if wildcard_rule not in ALL_DOMAINS:
            ALL_DOMAINS.add(wildcard_rule)
            print(f"✔ Added wildcard for news: {wildcard_rule}")

def fetch(url):
    if url in VISITED_URLS:
        return ""
    VISITED_URLS.add(url)
    try:
        return requests.get(url, headers=HEADERS, timeout=25).text
    except:
        return ""

def scrape_rss(feed_url):
    xml = fetch(feed_url)
    if not xml:
        return
    for link in re.findall(r"<link>(https?://[^<]+)</link>", xml):
        add_domain_from_url(link)

def scrape_links_recursive(url, depth=0):
    if depth > MAX_DEPTH:
        return
    html = fetch(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith("/"):
            base = '/'.join(url.split("/")[:3])
            full_url = base + href
        elif href.startswith("http"):
            full_url = href
        else:
            continue
        add_domain_from_url(full_url)
        if extract_domain(full_url) == extract_domain(url):
            scrape_links_recursive(full_url, depth + 1)
    time.sleep(0.3)

# ---------------- Seed news ----------------
NEWS_SEEDS = [
    "https://bbc.co.uk",
    "https://theguardian.com",
    "https://reuters.com",
    "https://apnews.com",
    "https://ft.com",
    "https://bloomberg.com",
    "https://metro.co.uk",
    "https://standard.co.uk",
    "https://nytimes.com",
    "https://cnn.com",
    "https://aljazeera.com",
    "https://google.com"  # keep Google
]

for s in NEWS_SEEDS:
    add_domain_from_url(s)

# ---------------- UK local ----------------
UK_LOCAL_SITES = [
    "manchestereveningnews.co.uk",
    "liverpoolecho.co.uk",
    "birminghammail.co.uk",
    "mylondon.news",
    "kentlive.news",
    "walesonline.co.uk",
    "chroniclelive.co.uk",
    "dailyrecord.co.uk",
    "insidecroydon.news"
]

for site in UK_LOCAL_SITES:
    add_domain_from_url(site)

# ---------------- English Google News RSS feeds ----------------
GOOGLE_NEWS_FEEDS = [
    "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss?hl=en-CA&gl=CA&ceid=CA:en",
    "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en",
    "https://news.google.com/rss?hl=en-IE&gl=IE&ceid=IE:en",
    "https://news.google.com/rss?hl=en-NZ&gl=NZ&ceid=NZ:en"
]

for feed in GOOGLE_NEWS_FEEDS:
    scrape_rss(feed)
    time.sleep(0.5)

# ---------------- social media ----------------
SOCIAL_SEEDS = [
    "https://facebook.com",
    "https://instagram.com",
    "https://x.com",
    "https://twitter.com",
    "https://youtube.com",
    "https://linkedin.com",
    "https://tiktok.com",
    "https://reddit.com",
    "https://discord.com",
    "https://telegram.org",
    "https://signal.org"
]

for s in SOCIAL_SEEDS:
    add_domain_from_url(s)

# ---------------- directories ----------------
DIRECTORY_SOURCES = [
    "https://www.w3newspapers.com/",
    "https://www.newspaperlists.com/",
    "https://www.thepaperboy.com/newspapers-by-country.cfm"
]

for src in DIRECTORY_SOURCES:
    scrape_links_recursive(src)

# ---------------- Write uBlock blocklist ----------------
sorted_domains = sorted(ALL_DOMAINS)
with open("h:\\ublock_blocklist.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted_domains))

print("✔ DONE")
print(f"✔ Total domains collected: {len(sorted_domains)}")
import requests
import tldextract
import re
import time
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (DomainHarvester)"}
ALL_DOMAINS = set()
VISITED_URLS = set()
MAX_DEPTH = 3  # recursion depth

ALLOWED_TLDS = (
    ".co.uk", ".org.uk", ".gov.uk", ".ac.uk",
    ".com", ".org", ".net", ".us",
    ".ca", ".com.au", ".net.au", ".org.au",
    ".ie", ".nz"
)

EXCLUDE_DOMAINS = [
    "wikipedia.org",
    "techradar.com",
    "engadget.com",
    "borninspace.com",
    "ign.com",
    "gamespot.com",
    "kotaku.com",
    "pcgamer.com",
    "eurogamer.net"
]

def clean_domain(domain):
    for p in ("www.", "m.", "amp."):
        if domain.startswith(p):
            domain = domain[len(p):]
    return domain

def extract_domain(url):
    try:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return clean_domain(f"{ext.domain}.{ext.suffix}")
    except:
        pass
    return None

def is_english_domain_or_news(url):
    d = extract_domain(url)
    # Allow if in allowed TLDs or contains "news" anywhere in the URL
    return (d and d.endswith(ALLOWED_TLDS)) or ("news" in url.lower())

def add_domain_from_url(url):
    if not url:
        return
    if any(exc in url for exc in EXCLUDE_DOMAINS):
        return
    if not is_english_domain_or_news(url):
        return
    d = extract_domain(url)
    if not d:
        return
    # Add uBlock wildcard format
    rule = f"||{d}^"
    if rule not in ALL_DOMAINS:
        ALL_DOMAINS.add(rule)
        print(f"✔ Added: {rule}")
    # Also check if "news" appears anywhere in the URL (subdomain or path)
    if "news" in url.lower() and d:
        wildcard_rule = f"||*.{d}^"
        if wildcard_rule not in ALL_DOMAINS:
            ALL_DOMAINS.add(wildcard_rule)
            print(f"✔ Added wildcard for news: {wildcard_rule}")

def fetch(url):
    if url in VISITED_URLS:
        return ""
    VISITED_URLS.add(url)
    try:
        return requests.get(url, headers=HEADERS, timeout=25).text
    except:
        return ""

def scrape_rss(feed_url):
    xml = fetch(feed_url)
    if not xml:
        return
    for link in re.findall(r"<link>(https?://[^<]+)</link>", xml):
        add_domain_from_url(link)

def scrape_links_recursive(url, depth=0):
    if depth > MAX_DEPTH:
        return
    html = fetch(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith("/"):
            base = '/'.join(url.split("/")[:3])
            full_url = base + href
        elif href.startswith("http"):
            full_url = href
        else:
            continue
        add_domain_from_url(full_url)
        if extract_domain(full_url) == extract_domain(url):
            scrape_links_recursive(full_url, depth + 1)
    time.sleep(0.3)

# ---------------- Seed news ----------------
NEWS_SEEDS = [
    "https://bbc.co.uk",
    "https://theguardian.com",
    "https://reuters.com",
    "https://apnews.com",
    "https://ft.com",
    "https://bloomberg.com",
    "https://metro.co.uk",
    "https://standard.co.uk",
    "https://nytimes.com",
    "https://cnn.com",
    "https://aljazeera.com",
    "https://google.com"  # keep Google
]

for s in NEWS_SEEDS:
    add_domain_from_url(s)

# ---------------- UK local ----------------
UK_LOCAL_SITES = [
    "manchestereveningnews.co.uk",
    "liverpoolecho.co.uk",
    "birminghammail.co.uk",
    "mylondon.news",
    "kentlive.news",
    "walesonline.co.uk",
    "chroniclelive.co.uk",
    "dailyrecord.co.uk",
    "insidecroydon.news"
]

for site in UK_LOCAL_SITES:
    add_domain_from_url(site)

# ---------------- English Google News RSS feeds ----------------
GOOGLE_NEWS_FEEDS = [
    "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss?hl=en-CA&gl=CA&ceid=CA:en",
    "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en",
    "https://news.google.com/rss?hl=en-IE&gl=IE&ceid=IE:en",
    "https://news.google.com/rss?hl=en-NZ&gl=NZ&ceid=NZ:en"
]

for feed in GOOGLE_NEWS_FEEDS:
    scrape_rss(feed)
    time.sleep(0.5)

# ---------------- social media ----------------
SOCIAL_SEEDS = [
    "https://facebook.com",
    "https://instagram.com",
    "https://x.com",
    "https://twitter.com",
    "https://youtube.com",
    "https://linkedin.com",
    "https://tiktok.com",
    "https://reddit.com",
    "https://discord.com",
    "https://telegram.org",
    "https://signal.org"
]

for s in SOCIAL_SEEDS:
    add_domain_from_url(s)

# ---------------- directories ----------------
DIRECTORY_SOURCES = [
    "https://www.w3newspapers.com/",
    "https://www.newspaperlists.com/",
    "https://www.thepaperboy.com/newspapers-by-country.cfm"
]

for src in DIRECTORY_SOURCES:
    scrape_links_recursive(src)

# ---------------- Write uBlock blocklist ----------------
sorted_domains = sorted(ALL_DOMAINS)
with open("h:\\ublock_blocklist.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted_domains))

print("✔ DONE")
print(f"✔ Total domains collected: {len(sorted_domains)}")
