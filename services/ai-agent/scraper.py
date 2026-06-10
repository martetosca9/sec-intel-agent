import requests
from bs4 import BeautifulSoup


class SecurityScraper:
    def __init__(self, base_url="https://thehackernews.com/"):
        self.base_url = base_url

    def fetch_news(self):
        """
        Fetches the latest news from the security blog.
        Returns a list of titles.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Basic selector for The Hacker News titles
            titles = [a.text.strip() for a in soup.select(".home-title")]
            
            return titles
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

if __name__ == "__main__":
    scraper = SecurityScraper()
    news = scraper.fetch_news()
    for i, title in enumerate(news, 1):
        print(f"{i}. {title}")
