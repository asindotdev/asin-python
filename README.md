# Asin Python SDK

The official Python SDK for the [Asin](https://www.asin.dev) Amazon price tracking API.

Track Amazon prices and products with a scheduled watchlist, price history, offers and alerts.

The SDK exposes **11 typed methods**, one per documented endpoint, with blocking and `asyncio` clients built on [HTTPX](https://www.python-httpx.org/), plus a generic `request()`.

## Requirements

- Python 3.11 or newer

## Installation

```sh
pip install asindotdev
```

## Get your API key

[Sign up for Asin](https://www.asin.dev/signup) or sign in, then copy your API key from the [dashboard](https://www.asin.dev/app). The client reads the `ASIN_API_KEY` environment variable when no key is passed.

## Quick start

```python
import os

from asin import AsinClient

with AsinClient(os.environ["ASIN_API_KEY"]) as client:
    response = client.search_amazon(query="wireless earbuds")
    print(response.data)
```

Keyword arguments mirror the [API reference](https://www.asin.dev/docs). Python keywords get a trailing underscore (`from_=`), and the wire name is used on the request.

## Async I/O

```python
import asyncio

from asin import AsyncAsinClient


async def main() -> None:
    async with AsyncAsinClient() as client:
        response = await client.search_amazon(query="wireless earbuds")
        print(response.data)


asyncio.run(main())
```

## HTTP methods

Each method uses the HTTP verb of its endpoint. `GET` and `DELETE` send parameters in the query string; `POST` and `PATCH` send them as a JSON body, except `wait` on `/products/{id}/check`, which stays in the query string. Null values are never sent, so `target_price` cannot be removed through the SDK yet.

`None` values are omitted, `False` and `0` are sent, and sequences repeat the parameter name.

## Any endpoint

```python
response = client.request("GET", "/account")
```

## Errors

```python
from asin import AsinAPIError

try:
    client.search_amazon(query="wireless earbuds")
except AsinAPIError as error:
    print(error.status, error, error.response_body)
```

| Error | When |
| --- | --- |
| `AsinConfigurationError` | Missing API key, invalid options, unsupported method, closed client. |
| `AsinSerializationError` | A required parameter is missing or a value can't be sent. |
| `AsinTransportError` | Network failure or timeout. |
| `AsinAPIError` | Non-2xx status (`status`, `error_message`, `response_body`, `raw_response`). |
| `AsinResponseDecodingError` | A success response could not be decoded. |

All of them extend `AsinError`.

## Retries

Requests are retried up to 3 times after a network error, a `408`, `429`, `500`, `502`, `503` or `504`. Other statuses, such as `400`, `401`, `402` or `404`, and client-side timeouts are not retried. The delay starts at 1 second and grows 1.5× per retry (capped at 30 seconds); a `Retry-After` header wins.

```python
client = AsinClient(max_retries=5, retry_delay=0.5)

# or for one request
client.search_amazon(query="wireless earbuds", request_options=RequestOptions(max_retries=0))
```

## Batch requests

`batch()` runs a function per item on 10 threads (`concurrency`) and returns one `BatchResult` per item, in input order. A failing item never stops the others. `AsyncAsinClient.batch()` does the same with `asyncio`.

```python
inputs = ["wireless earbuds", "mechanical keyboard", "usb-c hub"]
results = client.batch(inputs, lambda query: client.search_amazon(query=query), concurrency=5)

for result in results:
    if result.ok:
        print(result.value.data)
    else:
        print(inputs[result.index], result.error)
```

| Constant | Default | Description |
| --- | --- | --- |
| `DEFAULT_CONCURRENCY` | `10` | Tasks run at the same time by batch |
| `DEFAULT_TIMEOUT` | `120.0` | Request timeout (seconds) |
| `MAX_RETRIES` | `3` | Retry attempts after a network error, a 408/429/5xx |
| `RETRY_BACKOFF_FACTOR` | `1.5` | Exponential backoff multiplier |
| `DEFAULT_RETRY_DELAY` | `1.0` | Delay before the first retry (seconds) |

## Timeouts and custom HTTPX clients

```python
import httpx

from asin import AsinClient, RequestOptions

client = AsinClient(timeout=60)  # seconds, default 120, None disables
client.search_amazon(query="wireless earbuds", request_options=RequestOptions(timeout=30))

# Bring your own HTTPX client (proxies, limits, event hooks…). You keep ownership of it.
http_client = httpx.Client(proxy="http://localhost:8080")
client = AsinClient(http_client=http_client)
```

## Endpoints

11 methods, generated from the [OpenAPI document](https://www.asin.dev/openapi.json).

| Method | HTTP | Description |
| --- | --- | --- |
| `check_product()` | POST `/products/{id}/check` | Asks for a check right away (1 credit), at most once per 5 minutes; earlier calls return the product unchanged. A paused product has to be… |
| `delete_product()` | DELETE `/products/{id}` | Removes the product and its price history. |
| `fetch_offers()` | POST `/offers` | Reads the offers on Amazon for 1 credit, refunded if it doesn't answer. A read made in the last 3 hours, by anyone, is returned instead, fo… |
| `get_account()` | GET `/account` | Your plan, the credits left (monthly allowance and packs), how many products you track and the credits they use per month. |
| `get_asin_history()` | GET `/history` | Every price Asin read for an ASIN on a marketplace over the period, whoever tracks it, oldest first, with the lowest, highest and average o… |
| `get_offers()` | GET `/offers` | Who sells the product and at what price, as last read, cheapest first, with Amazon's own price and the cheapest new and used offers (used i… |
| `get_product()` | GET `/products/{id}` | The product's latest state and every price read of the period, oldest first. The history covers every read of this ASIN on this marketplace… |
| `list_products()` | GET `/products` | Your watchlist, newest first, with each product's latest state and its recent prices (trend). Filter with asin (and marketplace) to know if… |
| `search_amazon()` | GET `/search` | Amazon search results (up to 60, sponsored included), to find the ASIN of a product. Free, limited to 30 searches per hour. |
| `track_product()` | POST `/products` | Adds an ASIN, an Amazon link or a short link (amzn.to, a.co…) to your watchlist. The first check runs in the background within seconds (che… |
| `update_product()` | PATCH `/products/{id}` | Target price, drop alerts, check interval, or pause. Send only what changes. |

## License

MIT — see [LICENSE](LICENSE).
