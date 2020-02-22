from ir_utils import canonicalize, RELEVANT_KEYWORDS


def test_canonicalize():
    assert canonicalize("HTtP://www.Example.com/SomeFile.html") \
        == "example.com/SomeFile.html"
    assert canonicalize("http://www.example.com:80") \
        == "example.com/"
    assert canonicalize("https://www.example.com:443") \
        == "example.com/"
    assert canonicalize("https://www.example.com/a/../c.html") \
        == "example.com/c.html"
    assert canonicalize("http://www.example.com//a.html") \
        == "example.com/a.html"
    assert canonicalize("http://www.example.com/a.html#anything") \
        == "example.com/a.html"
    assert canonicalize("http://www.example.com/abc/?q1=abc") \
        == "example.com/abc/"
    assert canonicalize("http://www.example.com/abc?q1=abc") \
        == "example.com/abc"
    assert canonicalize("http://www.example.com/abc.html#section") \
        == "example.com/abc.html"
    assert canonicalize("http://www.example.com/abc?q1=abc#section") \
        == "example.com/abc"
    assert canonicalize("http://example.com/abc?q1=abc#section") \
        == "example.com/abc"


def test_relevant_keywords():
    assert isinstance(RELEVANT_KEYWORDS, set)