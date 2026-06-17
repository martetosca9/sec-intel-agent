from scraper import SecurityScraper


def test_fetch_news_structure():
    scraper = SecurityScraper()
    # We won't actually hit the network in a strict CI environment,
    # but for this initial setup, we verify the method exists and returns a list.
    news = scraper.fetch_news()
    assert isinstance(news, list)

def test_fetch_article_content():
    scraper = SecurityScraper()
    # Test with a known URL from The Hacker News
    url = "https://thehackernews.com/2024/05/new-android-malware-using-ocr-to.html"
    content = scraper.fetch_article_content(url)
    assert isinstance(content, str)
    # If the network is available, it should ideally not be empty
