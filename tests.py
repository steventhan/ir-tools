from ir_utils import canonicalize


def test_canonicalize():
    assert canonicalize("HTtP://www.Example.com/SomeFile.html") \
        == "www.example.com/SomeFile.html"
    assert canonicalize("http://www.example.com:80") \
        == "www.example.com/"
    assert canonicalize("https://www.example.com:443") \
        == "www.example.com/"
    assert canonicalize("https://www.example.com/a/../c.html") \
        == "www.example.com/c.html"
    assert canonicalize("http://www.example.com//a.html") \
        == "www.example.com/a.html"
    assert canonicalize("http://www.example.com/a.html#anything") \
        == "www.example.com/a.html"
    assert canonicalize("http://www.example.com/abc/?q1=abc") \
        == "www.example.com/abc/"
    assert canonicalize("http://www.example.com/abc?q1=abc") \
        == "www.example.com/abc"
    assert canonicalize("http://www.example.com/abc.html#section") \
        == "www.example.com/abc.html"
    assert canonicalize("http://www.example.com/abc?q1=abc#section") \
        == "www.example.com/abc"
