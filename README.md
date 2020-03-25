# ir-utils
## Installation
`pip install  git+https://github.com/steventhan/ir-utils.git -U`
## Examples
```python
from ir_utils import canonicalize, RELEVANT_KEYWORDS

print(canonicalize("https://hello.com:443/abc.html?q1=test#main")) # Prints hello.com/abc.html
print(RELENVANT_KEYWORDS)

```

## Merging local and remote indices
```python
from ir_utils import merge_es 


def transform(doc: dict):
    return {
        "body": doc["body"],
        "url": doc["url"],
        "wave": doc["wave"],
        "outlinks": doc["outlinks"],
        "inlinks": doc["inlinks"],
        "crawler": doc["crawler"]
    }

merge_es("http://localhost:9200", "crawler", remote_index="crawler1", 
    doc_transform_func=transform)
```

## Non-es merge
```python
from ir_utils import merge_non_es

lst = [
    {
        "_id": "example.com/abc.html",
        "body": "the page body",
        "url": "https://example.com/abc.html",
        "wave": -1,
        "outlinks": [...],
        "inlinks": [...],
        "crawler": "cralwer name"
    },
    ...
]

merge_non_es(lst)
```
