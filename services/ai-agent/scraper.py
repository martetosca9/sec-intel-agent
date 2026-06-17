import requests
from bs4 import BeautifulSoup

class SecurityScraper:
    def __init__(self, base_url="https://thehackernews.com/"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_article_content(self, url):
        """
        Visits the article URL and extracts the main text content.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # The Hacker News uses a div with class 'articlebody' or id 'articlebody'
            content_div = soup.select_one(".articlebody") or soup.select_one("#articlebody")
            
            if content_div:
                # Remove script and style elements
                for script_or_style in content_div(["script", "style"]):
                    script_or_style.decompose()
                return content_div.get_text(separator="\n").strip()
            return ""
        except Exception as e:
            print(f"Error fetching article content from {url}: {e}")
            return ""

    def fetch_news(self, fetch_full_content=False):
        """
        Fetches the latest news from the security blog.
        Returns a list of dictionaries with title, link, summary, and optionally full_content.
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []

            # Selector for the main post containers in The Hacker News
            posts = soup.select(".body-post")

            for post in posts:
                title_elem = post.select_one(".home-title")
                link_elem = post.select_one(".story-link")
                desc_elem = post.select_one(".home-desc")

                if title_elem and link_elem:
                    url = link_elem.get("href")
                    item = {
                        "title": title_elem.text.strip(),
                        "link": url,
                        "summary": desc_elem.text.strip() if desc_elem else ""
                    }
                    
                    if fetch_full_content:
                        print(f"Fetching full content for: {item['title']}...")
                        item["full_content"] = self.fetch_article_content(url)
                    
                    news_items.append(item)

            return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

if __name__ == "__main__":
    scraper = SecurityScraper()
    # Test with one article for efficiency in terminal output
    news = scraper.fetch_news(fetch_full_content=True)
    if news:
        item = news[0]
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Full Content Snippet: {item.get('full_content', '')[:300]}...\n")

