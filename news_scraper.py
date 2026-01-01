import requests
import tldextract
import re
import time
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (DomainHarvester)"}
ALL_DOMAINS = set()
VISITED_URLS = set()
MAX_DEPTH = 3  # recursion depth

# ---------------- allowed English-language TLDs ----------------
ALLOWED_TLDS = (
    # UK
    ".co.uk", ".org.uk", ".gov.uk", ".ac.uk",
    # US / global English
    ".com", ".org", ".net", ".us",
    # Canada
    ".ca",
    # Australia
    ".com.au", ".net.au", ".org.au",
    # Ireland
    ".ie",
    # New Zealand
    ".nz"
)

# ---------------- exclusions ----------------
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

# ---------------- helpers ----------------
def extract_domain(url):
    try:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}".lower()
    except:
        pass
    return None

def is_english_domain(domain):
    return domain.endswith(ALLOWED_TLDS)

def add_domain(url):
    d = extract_domain(url)
    if not d:
        return
    if not is_english_domain(d):
        return
    if any(exc in d for exc in EXCLUDE_DOMAINS):
        return
    if d not in ALL_DOMAINS:
        ALL_DOMAINS.add(d)
        print(f"✔ Added: {d} | Total domains: {len(ALL_DOMAINS)}")

def fetch(url):
    if url in VISITED_URLS:
        return ""
    VISITED_URLS.add(url)
    try:
        return requests.get(url, headers=HEADERS, timeout=25).text
    except:
        return ""

# ---------------- scrape RSS ----------------
def scrape_rss(feed_url):
    xml = fetch(feed_url)
    if not xml:
        return
    for link in re.findall(r"<link>(https?://[^<]+)</link>", xml):
        add_domain(link)

# ---------------- recursive scraping ----------------
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
            base = "/".join(url.split("/")[:3])
            full_url = base + href
        elif href.startswith("http"):
            full_url = href
        else:
            continue

        add_domain(full_url)

        if extract_domain(full_url) == extract_domain(url):
            scrape_links_recursive(full_url, depth + 1)

    time.sleep(0.3)

# ---------------- seed news ----------------
NEWS_SEEDS = [
    "https://bbc.co.uk",
    "https://bbc.com",
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
    "https://news.sky.com",
    "https://dailymail.co.uk",
    "https://telegraph.co.uk",
    "https://thetimes.co.uk",
    "https://thesun.co.uk",
    "https://express.co.uk",
    "https://mirror.co.uk",
    "https://talktv.co.uk"
]

for s in NEWS_SEEDS:
    add_domain(s)

# ---------------- UK local / regional ----------------
UK_LOCAL_SITES = [
    "manchestereveningnews.co.uk",
    "liverpoolecho.co.uk",
    "birminghammail.co.uk",
    "mylondon.news",
    "kentlive.news",
    "walesonline.co.uk",
    "chroniclelive.co.uk",
    "dailyrecord.co.uk",
    "insidecroydon.com",
    "essexlive.news",
    "plymouthherald.co.uk",
    "glasgowlive.co.uk",
    "edinburghnews.scotsman.com",
    "bristolpost.co.uk"
]

for site in UK_LOCAL_SITES:
    add_domain(site)

# ---------------- social media ----------------
SOCIAL_SEEDS = [
    "https://facebook.com",
    "https://instagram.com",
    "https://threads.net",
    "https://x.com",
    "https://twitter.com",
    "https://youtube.com",
    "https://linkedin.com",
    "https://tiktok.com",
    "https://snapchat.com",
    "https://reddit.com",
    "https://quora.com",
    "https://discord.com",
    "https://telegram.org",
    "https://signal.org",
    "https://twitch.tv",
    "https://rumble.com",
    "https://truthsocial.com",
    "https://gab.com",
    "https://parler.com",
    "mastodon.social",
    "lemmy.world",
    "pixelfed.social",
    "peertube.social"
]

for s in SOCIAL_SEEDS:
    add_domain(s)

# ---------------- Google News RSS feeds (English) ----------------
GOOGLE_NEWS_FEEDS = [
    "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss?hl=en-CA&gl=CA&ceid=CA:en",
    "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en",
    "https://news.google.com/rss?hl=en-IE&gl=IE&ceid=IE:en",
    "https://news.google.com/rss?hl=en-NZ&gl=NZ&ceid=NZ:en"
]

for feed in GOOGLE_NEWS_FEEDS:
    print(f"Scraping RSS: {feed}")
    scrape_rss(feed)
    time.sleep(0.5)

# ---------------- directories ----------------
DIRECTORY_SOURCES = [
    "https://www.w3newspapers.com/",
    "https://www.newspaperlists.com/",
    "https://www.thepaperboy.com/newspapers-by-country.cfm"
]

for src in DIRECTORY_SOURCES:
    print(f"Scraping directory: {src}")
    scrape_links_recursive(src)

# ---------------- publisher-side RSS feeds ----------------
PUBLISHER_RSS_FEEDS = [
    "https://feeds.skynews.com/feeds/rss/home.xml",
    "https://www.telegraph.co.uk/rss.xml",
    "https://www.theguardian.com/uk/rss",
    "https://www.dailymail.co.uk/articles.rss",
    "https://www.ft.com/?format=rss"
]

for feed in PUBLISHER_RSS_FEEDS:
    print(f"Scraping publisher RSS: {feed}")
    scrape_rss(feed)
    time.sleep(0.5)

# ---------------- uBlock output ----------------
sorted_domains = sorted(ALL_DOMAINS)

with open("ublock_blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! uBlock Origin – English News & Social Blocklist\n")
    f.write("! One-time generated\n\n")
    for d in sorted_domains:
        f.write(f"||{d}^\n")

print("✔ DONE")
print(f"✔ Total domains collected: {len(sorted_domains)}")
print("✔ Output written to ublock_blocklist.txt")
