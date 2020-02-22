# ir-utils
## Installation
`pip install  git+https://github.com/steventhan/ir-utils.git`
## Example
```python
from ir_utils import canonicalize

print(canonicalize("https://hello.com:443/abc.html?q1=test#main")) # Prints https://hello.com/abc.html

```
