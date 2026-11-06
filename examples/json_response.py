"""Call the featured endpoint and print the JSON result."""

import json
import os

from asin import AsinClient

with AsinClient(os.environ["ASIN_API_KEY"]) as client:
    response = client.search_amazon(query="wireless earbuds")
    print(json.dumps(response.data, indent=2))
