from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import httpx
import pytest

from asin import (
    ENDPOINTS,
    AsinAPIError,
    AsinClient,
    AsinConfigurationError,
    AsinResponseDecodingError,
    AsinSerializationError,
    AsinTransportError,
    AsyncAsinClient,
    BinaryResponse,
    JsonResponse,
    RequestOptions,
)

Responder = Callable[[httpx.Request], httpx.Response]


def _json(body: Any, status: int = 200) -> httpx.Response:
    return httpx.Response(status, json=body)


def _client(
    responder: Responder = lambda _r: _json({"ok": True}), **kwargs: Any
) -> tuple[AsinClient, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return responder(request)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    kwargs.setdefault("api_key", "test-key")
    return AsinClient(http_client=http_client, **kwargs), requests


def test_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ASIN_API_KEY", raising=False)
    with pytest.raises(AsinConfigurationError, match="ASIN_API_KEY"):
        AsinClient()
    with pytest.raises(AsinConfigurationError):
        AsinClient("   ")


def test_reads_api_key_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ASIN_API_KEY", "env-key")
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _json({})

    with AsinClient(http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.request("GET", "/account")
    assert requests[0].headers["authorization"] == "Bearer env-key"


def test_rejects_invalid_configuration() -> None:
    with pytest.raises(AsinConfigurationError):
        AsinClient("k", base_url="ftp://example.test")
    with pytest.raises(AsinConfigurationError):
        AsinClient("k", timeout=0)


def test_featured_operation_sends_get_with_api_key() -> None:
    client, requests = _client(lambda _r: _json({"hello": "world"}))
    response = client.search_amazon(query="wireless earbuds")
    assert isinstance(response, JsonResponse)
    assert response.data == {"hello": "world"}
    request = requests[0]
    assert request.method == "GET"
    assert str(request.url).split("?")[0] == "https://www.asin.dev/api/v1/search"
    assert request.headers["authorization"] == "Bearer test-key"
    assert request.headers["user-agent"].startswith("asin-python/")


def test_query_serialization() -> None:
    client, requests = _client(base_url="https://example.test/")
    client.request(
        "GET",
        "/anything",
        {
            "text": "a b&c",
            "flag": False,
            "count": 0,
            "ratio": 1.5,
            "whole": 2.0,
            "list": ["x", "y"],
            "nothing": None,
        },
    )
    url = urlsplit(str(requests[0].url))
    assert url.netloc == "example.test"
    assert parse_qsl(url.query) == [
        ("text", "a b&c"),
        ("flag", "false"),
        ("count", "0"),
        ("ratio", "1.5"),
        ("whole", "2"),
        ("list", "x"),
        ("list", "y"),
    ]


def test_post_sends_json_body() -> None:
    client, requests = _client()
    client.request("POST", "/anything", {"query": "x", "page": 2, "gone": None})
    request = requests[0]
    assert request.method == "POST"
    assert request.headers["content-type"] == "application/json"
    assert json.loads(request.content) == {"query": "x", "page": 2}
    assert request.url.query == b""


def test_wait_location_depends_on_the_endpoint() -> None:
    client, requests = _client()
    client.request("POST", "/products/{id}/check", {"id": "p1", "wait": True})
    assert requests[0].url.query == b"wait=true"
    assert json.loads(requests[0].content) == {}
    client.request("POST", "/products", {"product": "B09DFCB66S", "wait": True})
    assert requests[1].url.query == b""
    assert json.loads(requests[1].content) == {"product": "B09DFCB66S", "wait": True}


def test_patch_and_delete() -> None:
    client, requests = _client()
    client.request("PATCH", "/products/{id}", {"id": "p1", "paused": True})
    assert requests[0].method == "PATCH"
    assert json.loads(requests[0].content) == {"paused": True}
    client.request("DELETE", "/products/{id}", {"id": "p1"})
    assert requests[1].method == "DELETE"
    assert requests[1].content == b""


def test_path_parameters() -> None:
    client, requests = _client()
    client.request("GET", "/items/{id}", {"id": "a/b c", "other": 1})
    assert requests[0].url.raw_path == b"/api/v1/items/a%2Fb%20c?other=1"
    with pytest.raises(AsinSerializationError):
        client.request("GET", "/items/{id}", {})


def test_unsupported_method_is_rejected() -> None:
    client, requests = _client()
    with pytest.raises(AsinConfigurationError):
        client.get_account(request_options=RequestOptions(method="POST"))
    assert requests == []


@pytest.mark.parametrize("name", sorted(ENDPOINTS))
def test_every_endpoint_method(name: str) -> None:
    client, requests = _client(lambda _r: _json({}))
    method = getattr(client, name + "_" if not hasattr(client, name) else name)
    kwargs: dict[str, Any] = REQUIRED.get(name, {})
    method(**kwargs)
    endpoint = ENDPOINTS[name]
    expected = endpoint.path.replace("{id}", "test")
    assert requests[0].url.path == "/api/v1" + expected
    assert requests[0].method == endpoint.methods[0]


def test_binary_response() -> None:
    client, _ = _client(
        lambda _r: httpx.Response(200, content=b"\x89PNG", headers={"content-type": "image/png"})
    )
    response = client.request("GET", "/anything")
    assert isinstance(response, BinaryResponse)
    assert response.bytes == b"\x89PNG"
    assert response.content_type == "image/png"


def test_non_json_success_for_json_operation() -> None:
    client, _ = _client(
        lambda _r: httpx.Response(200, content=b"<html>", headers={"content-type": "text/html"})
    )
    with pytest.raises(AsinResponseDecodingError):
        client.search_amazon(query="wireless earbuds")


def test_api_error() -> None:
    client, _ = _client(lambda _r: _json({"error": "Invalid API Key"}, 401))
    with pytest.raises(AsinAPIError) as info:
        client.request("GET", "/account")
    assert info.value.status == 401
    assert str(info.value) == "Invalid API Key"
    assert info.value.response_body == {"error": "Invalid API Key"}


def test_non_json_error_body() -> None:
    client, _ = _client(lambda _r: httpx.Response(502, content=b"Bad gateway"), max_retries=0)
    with pytest.raises(AsinAPIError) as info:
        client.request("GET", "/account")
    assert info.value.status == 502
    assert info.value.raw_response.body == b"Bad gateway"


def test_transport_error() -> None:
    def fail(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down")

    client, _ = _client(fail, max_retries=0)
    with pytest.raises(AsinTransportError):
        client.request("GET", "/account")


def test_closed_client() -> None:
    client, _ = _client()
    client.close()
    with pytest.raises(AsinConfigurationError):
        client.request("GET", "/account")


@pytest.mark.asyncio
async def test_async_client() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _json({"async": True})

    async with AsyncAsinClient(
        "k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    ) as client:
        response = await client.search_amazon(query="wireless earbuds")
    assert isinstance(response, JsonResponse)
    assert response.data == {"async": True}
    assert requests[0].headers["authorization"] == "Bearer k"


def test_retries_then_succeeds() -> None:
    statuses = [503, 429, 200]
    client, requests = _client(lambda _r: _json({"ok": True}, statuses.pop(0)), retry_delay=0.001)
    response = client.request("GET", "/account")
    assert isinstance(response, JsonResponse)
    assert len(requests) == 3


def test_gives_up_after_max_retries() -> None:
    client, requests = _client(
        lambda _r: _json({"error": "busy"}, 503), retry_delay=0.001, max_retries=2
    )
    with pytest.raises(AsinAPIError):
        client.request("GET", "/account")
    assert len(requests) == 3


def test_never_retries_client_errors() -> None:
    client, requests = _client(
        lambda _r: _json({"error": "Payment required"}, 402), retry_delay=0.001
    )
    with pytest.raises(AsinAPIError):
        client.request("GET", "/account")
    assert len(requests) == 1


def test_retries_network_errors_and_retry_after() -> None:
    calls = {"n": 0}

    def flaky(_request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("reset")
        if calls["n"] == 2:
            return httpx.Response(429, json={}, headers={"retry-after": "0"})
        return _json({"ok": True})

    client, _ = _client(flaky, retry_delay=0.001)
    client.request("GET", "/account")
    assert calls["n"] == 3


@pytest.mark.parametrize(
    ("message", "expected_calls"),
    [
        ("Rate limit exceeded: You've exceeded the rate limit on your subscription", 1),
        ("Rate limit exceeded for the API key: quota daily", 1),
        ("Invalid API Key", 1),
    ],
)
def test_401_is_never_retried(message: str, expected_calls: int) -> None:
    calls = {"n": 0}

    def respond(_request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return _json({"error": message}, 401) if calls["n"] == 1 else _json({"ok": True})

    client, requests = _client(respond, retry_delay=0.001)
    try:
        client.request("GET", "/account")
    except AsinAPIError:
        pass
    assert len(requests) == expected_calls


def test_nested_error_message() -> None:
    client, _ = _client(
        lambda _r: _json(
            {"error": {"code": "insufficient_credits", "message": "No credits left"}}, 402
        )
    )
    with pytest.raises(AsinAPIError) as info:
        client.get_account()
    assert info.value.error_message == "No credits left"


def test_request_level_retry_override() -> None:
    client, requests = _client(lambda _r: _json({}, 500), retry_delay=0.001)
    with pytest.raises(AsinAPIError):
        client.request("GET", "/account", max_retries=0)
    assert len(requests) == 1


def test_batch_keeps_order_and_isolates_failures() -> None:
    client, requests = _client(lambda r: _json({"q": r.url.params["q"]}))

    def task(q: str) -> Any:
        if q == "bad":
            raise ValueError("boom")
        return client.request("GET", "/account", {"q": q})

    results = client.batch(["a", "bad", "c"], task, concurrency=2)
    assert [r.index for r in results] == [0, 1, 2]
    assert [r.ok for r in results] == [True, False, True]
    assert isinstance(results[1].error, ValueError)
    assert len(requests) == 2
    with pytest.raises(AsinConfigurationError):
        client.batch([1], lambda x: x, concurrency=0)


@pytest.mark.asyncio
async def test_async_batch_caps_concurrency() -> None:
    import asyncio

    async with AsyncAsinClient(
        "k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(lambda r: _json({})))
    ) as client:
        running = peak = 0

        async def task(n: int) -> int:
            nonlocal running, peak
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0.005)
            running -= 1
            return n * 10

        results = await client.batch(range(6), task, concurrency=2)
    assert peak == 2
    assert [r.value for r in results] == [0, 10, 20, 30, 40, 50]


REQUIRED: dict[str, dict[str, Any]] = {
    "check_product": {"id": "test"},
    "delete_product": {"id": "test"},
    "fetch_offers": {"asin": "test"},
    "get_asin_history": {"asin": "test"},
    "get_offers": {"asin": "test"},
    "get_product": {"id": "test"},
    "search_amazon": {"query": "test"},
    "track_product": {"product": "test"},
    "update_product": {"id": "test"},
}
