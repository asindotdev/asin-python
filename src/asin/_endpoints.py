"""Generated from the Asin OpenAPI document. Do not edit by hand."""

from __future__ import annotations

from .models import EndpointDefinition

ENDPOINTS: dict[str, EndpointDefinition] = {
    "check_product": EndpointDefinition(
        path="/products/{id}/check",
        methods=("POST",),
        response="json",
        required=("id",),
    ),
    "delete_product": EndpointDefinition(
        path="/products/{id}",
        methods=("DELETE",),
        response="json",
        required=("id",),
    ),
    "fetch_offers": EndpointDefinition(
        path="/offers",
        methods=("POST",),
        response="json",
        required=("asin",),
    ),
    "get_account": EndpointDefinition(
        path="/account",
        methods=("GET",),
        response="json",
        required=(),
    ),
    "get_asin_history": EndpointDefinition(
        path="/history",
        methods=("GET",),
        response="json",
        required=("asin",),
    ),
    "get_offers": EndpointDefinition(
        path="/offers",
        methods=("GET",),
        response="json",
        required=("asin",),
    ),
    "get_product": EndpointDefinition(
        path="/products/{id}",
        methods=("GET",),
        response="json",
        required=("id",),
    ),
    "list_products": EndpointDefinition(
        path="/products",
        methods=("GET",),
        response="json",
        required=(),
    ),
    "search_amazon": EndpointDefinition(
        path="/search",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "track_product": EndpointDefinition(
        path="/products",
        methods=("POST",),
        response="json",
        required=("product",),
    ),
    "update_product": EndpointDefinition(
        path="/products/{id}",
        methods=("PATCH",),
        response="json",
        required=("id",),
    ),
}
