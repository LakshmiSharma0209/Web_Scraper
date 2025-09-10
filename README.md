# News Article Scraper & Analyzer

This Python script is a simple web scraper that fetches news article headlines and links from a specified URL, performs data analysis on the extracted text, and generates a visualization of the most common words.

## 🚀 Features

- **Web Scraping:** Fetches HTML content from a website using the `requests` library.
- **HTML Parsing:** Uses `BeautifulSoup` to parse the HTML and extract relevant data (article titles and links).
- **Text Analysis:** Utilizes the `re` and `collections.Counter` libraries to count the frequency of words in the scraped headlines.
- **Data Handling:** Manages and processes the scraped data using the `pandas` library.
- **Data Visualization:** Generates a bar chart of the most common words using `matplotlib.pyplot`.
- **File Output:** Saves the scraped data to a `.csv` file and the visualization to a `.png` file.

## 💻 How It Works

The script is divided into two main functions:

1.  `scrape_news_articles(url)`: This function sends an HTTP GET request to the provided URL, parses the HTML, and attempts to find and extract news article headlines and their corresponding links. For debugging purposes, it saves the raw HTML content to `debug_page.html`.
2.  `analyze_news_data(news_data)`: This function takes the list of scraped articles, converts it into a pandas DataFrame, and performs a simple text analysis. It identifies the top 10 most common words in the headlines and creates a bar chart visualization.

The main execution block calls these functions sequentially, saving the output to `news_data.csv` and `news_analysis.png`.

## 📦 Requirements

Before running the script, you need to install the required Python libraries. You can do this using pip:

```bash
pip install requests beautifulsoup4 pandas matplotlib
