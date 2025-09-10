import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re


def scrape_news_articles(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("Saved HTML to debug_page.html for inspection")

        selectors = [
            "table.itemlist",
            "table#hnmain",
            "tr.athing",
            "a.titlelink",
            '[class*="title"]',
            'a[href*="item?id="]',
        ]

        for selector in selectors:
            elements = soup.select(selector)
            print(f"Selector '{selector}': found {len(elements)} elements")
            if elements:
                break

        all_links = soup.find_all("a", href=True)
        news_links = []

        for link in all_links:
            href = link["href"]
            text = link.get_text().strip()
            if text and len(text) > 10 and ("http" in href or "item?id=" in href):
                news_links.append({"text": text, "href": href})

        print(f"Found {len(news_links)} potential news links")

        return news_links[:10]

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        import traceback

        traceback.print_exc()
        return []


def analyze_news_data(news_data):
    df = pd.DataFrame(news_data)

    if df.empty:
        print("No data to analyze")
        return df

    print(f"Total articles scraped: {len(df)}")
    print("\nFirst few articles:")
    print(df.head())

    print(f"\nAvailable columns: {list(df.columns)}")

    headline_col = "headline" if "headline" in df.columns else "text"

    all_headlines = " ".join(df[headline_col]).lower()
    words = re.findall(r"\b[a-zA-Z]{3,}\b", all_headlines)
    word_counts = Counter(words).most_common(10)

    print(f"\nMost common words in {headline_col}:")
    for word, count in word_counts:
        print(f"{word}: {count}")

    if not df.empty:
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        if word_counts:
            words, counts = zip(*word_counts)
            plt.bar(words, counts, color="lightcoral")
            plt.title("Top Words in Headlines")
            plt.xticks(rotation=45, ha="right")
        else:
            plt.text(0.5, 0.5, "No words found", ha="center", va="center")
            plt.title("No Word Data")

        plt.subplot(1, 2, 2)
        plt.text(
            0.5,
            0.5,
            f"Scraped {len(df)} articles\nFrom Hacker News",
            ha="center",
            va="center",
            fontsize=12,
        )
        plt.title("Scraping Results")
        plt.axis("off")

        plt.tight_layout()
        plt.savefig("news_analysis.png")
        print("Visualization saved to 'news_analysis.png'")
        plt.close()

    return df


if __name__ == "__main__":
    url = "https://news.ycombinator.com/"

    print("Starting web scraper...")
    news_data = scrape_news_articles(url)

    if news_data:
        print(f"Successfully scraped {len(news_data)} articles")
        df = analyze_news_data(news_data)
        df.to_csv("news_data.csv", index=False)
        print("Data saved to 'news_data.csv'")
    else:
        print("No articles were scraped.")
