from url_normalize import url_normalize
from urllib.parse import urlparse, urljoin


def canonicalize(url: str) -> str:
    normalized = url_normalize(url)
    parsed = urlparse(normalized)
    return urljoin(normalized, parsed.path) \
        .replace("http://", "").replace("https://", "")


if __name__ == "__main__":
    print(canonicalize("https://example.com/123/"))