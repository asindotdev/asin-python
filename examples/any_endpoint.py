"""Call any path with request() and handle API errors."""

from asin import AsinAPIError, AsinClient, JsonResponse

with AsinClient() as client:  # reads ASIN_API_KEY
    try:
        response = client.request("GET", "/account")
        if isinstance(response, JsonResponse):
            print(response.data)
    except AsinAPIError as error:
        print(f"HTTP {error.status}: {error}")
