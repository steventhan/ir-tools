from url_normalize import url_normalize
from urllib.parse import urlparse, urljoin


def canonicalize(url: str) -> str:
    normalized = url_normalize(url)
    parsed = urlparse(normalized)
    url_no_scheme = urljoin(normalized, parsed.path) \
        .replace("http://", "").replace("https://", "")
    return url_no_scheme[4:] if url_no_scheme.startswith("www.") \
        else url_no_scheme


if __name__ == "__main__":
    print(canonicalize("https://example.com/123/"))