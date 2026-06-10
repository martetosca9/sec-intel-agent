from scraper import SecurityScraper


def test_fetch_news_structure():
    scraper = SecurityScraper()
    # We won't actually hit the network in a strict CI environment,
    # but for this initial setup, we verify the method exists and returns a list.
    news = scraper.fetch_news()
    assert isinstance(news, list)
