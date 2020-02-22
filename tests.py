from ir_utils import canonicalize


def test_canonicalize():
    assert canonicalize("HTTP://www.Example.com/SomeFile.html") \
        == "http://www.example.com/SomeFile.html"
    assert canonicalize("http://www.example.com:80") \
        == "http://www.example.com/"
    assert canonicalize("https://www.example.com:443") \
        == "https://www.example.com/"
    assert canonicalize("http://www.example.com/a/../c.html") \
        == "http://www.example.com/c.html"
    assert canonicalize("http://www.example.com//a.html") \
        == "http://www.example.com/a.html"
    assert canonicalize("http://www.example.com/a.html#anything") \
        == "http://www.example.com/a.html"
    assert canonicalize("http://www.example.com/abc/?q1=abc") \
        == "http://www.example.com/abc/"
    assert canonicalize("http://www.example.com/abc?q1=abc") \
        == "http://www.example.com/abc"
    assert canonicalize("http://www.example.com/abc.html#section") \
        == "http://www.example.com/abc.html"
    assert canonicalize("http://www.example.com/abc?q1=abc#section") \
        == "http://www.example.com/abc"
