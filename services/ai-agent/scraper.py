import requests
from bs4 import BeautifulSoup

class SecurityScraper:
    def __init__(self, base_url="https://thehackernews.com/"):
        self.base_url = base_url

    def fetch_news(self):
        """
        Fetches the latest news from the security blog.
        Returns a list of dictionaries with title, link, and summary.
        """
        try:
            response = requests.get(self.base_url)
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
                    news_items.append({
                        "title": title_elem.text.strip(),
                        "link": link_elem.get("href"),
                        "summary": desc_elem.text.strip() if desc_elem else ""
                    })

            return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

if __name__ == "__main__":
    scraper = SecurityScraper()
    news = scraper.fetch_news()
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']}")
        print(f"   Link: {item['link']}")
        print(f"   Summary: {item['summary'][:100]}...\n")

