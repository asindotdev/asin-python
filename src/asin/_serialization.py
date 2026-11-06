"""Request serialization: path filling, query pairs and JSON bodies."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlencode

from .errors import AsinSerializationError
from .models import HTTPMethod

_PATH_PARAM = re.compile(r"\{([^}]+)\}")
# The API reads the global parameters from the query string, whatever the method.
QUERY_STRING_PARAMS = {"/products/{id}/check": ("wait",)}


@dataclass(frozen=True, slots=True)
class SerializedRequest:
    path: str
    query: list[tuple[str, str]]
    body: dict[str, Any] | None


def serialize_request(
    method: HTTPMethod, path_template: str, params: Mapping[str, Any] | None
) -> SerializedRequest:
    """Fill ``{name}`` path segments, then send the rest as query pairs (GET, DELETE) or a JSON body (POST, PATCH).

    ``wait`` stays in the query string on POST /products/{id}/check.

    ``None`` values and empty sequences are omitted; ``False`` and ``0`` are sent.
    """

    if params is not None and not isinstance(params, Mapping):
        raise AsinSerializationError("Request parameters must be a mapping.")
    remaining = {name: value for name, value in (params or {}).items() if value is not None}

    def fill(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in remaining:
            raise AsinSerializationError(f'The "{name}" path parameter is required.', name)
        return quote(to_wire_string(name, remaining.pop(name)), safe="")

    path = _PATH_PARAM.sub(fill, path_template)

    if method in ("GET", "DELETE"):
        query: list[tuple[str, str]] = []
        for name, value in remaining.items():
            if isinstance(value, (list, tuple)):
                query.extend(
                    (name, to_wire_string(name, item)) for item in value if item is not None
                )
            else:
                query.append((name, to_wire_string(name, value)))
        return SerializedRequest(path=path, query=query, body=None)

    query = [
        (name, to_wire_string(name, remaining.pop(name)))
        for name in QUERY_STRING_PARAMS.get(path_template, ())
        if name in remaining
    ]
    for name, value in remaining.items():
        if isinstance(value, float) and not math.isfinite(value):
            raise AsinSerializationError(f'The "{name}" parameter must be a finite number.', name)
    return SerializedRequest(path=path, query=query, body=remaining)


def to_wire_string(name: str, value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise AsinSerializationError(f'The "{name}" parameter must be a finite number.', name)
        return str(int(value)) if value.is_integer() else repr(value)
    if isinstance(value, (Mapping, list, tuple)):
        try:
            return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
        except (TypeError, ValueError) as cause:
            raise AsinSerializationError(
                f'The "{name}" parameter could not be serialized.', name
            ) from cause
    raise AsinSerializationError(
        f'The "{name}" parameter has an unsupported type ({type(value).__name__}).', name
    )


def encode_query(pairs: list[tuple[str, str]]) -> str:
    return urlencode(pairs, quote_via=quote)


def encode_json_body(body: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(body, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as cause:
        raise AsinSerializationError("The request body could not be serialized as JSON.") from cause
