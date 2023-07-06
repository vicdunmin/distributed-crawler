from ..src.youtube import get_comments_from_url, get_trending_urls

def test_get_url_all():
    """test for getting correct urls"""
    urls = get_trending_urls()
    for url in urls:
        assert url.startswith("https://youtube.com/watch?v=")

def test_get_url_until():
    """test for getting a specified number of urls"""
    n = 10
    urls = get_trending_urls(10)
    assert len(urls) == n

def test_get_comments():
    """test for getting a specified number of comments"""
    n = 10
    url = get_trending_urls(10)[2]
    comments = get_comments_from_url(url, n)
    assert len(comments) == n

