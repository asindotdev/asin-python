"""Generated from the Asin OpenAPI document. Do not edit by hand."""

from __future__ import annotations

from typing import Any, Literal, cast

from .models import APIResponse, JsonResponse, RequestOptions


class _SyncOperations:
    """Generated Asin endpoint methods."""

    __slots__ = ()

    def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        raise NotImplementedError

    def check_product(
        self,
        *,
        id: str,
        wait: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Check the price now. Asks for a check right away (1 credit), at most once per 5 minutes; earlier calls return the product unchanged. A paused product has to be resumed first. The check runs in the background; with wait=true the answer waits for it. Read last_e…

        ``POST /products/{id}/check``

        Args:
            id: product_id returned when the product was added
            wait: Answer once the check is done (up to 45 seconds)
        """
        return cast(
            JsonResponse, self._call("check_product", {"id": id, "wait": wait}, request_options)
        )

    def delete_product(
        self,
        *,
        id: str,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Stop tracking a product. Removes the product and its price history.

        ``DELETE /products/{id}``

        Args:
            id: product_id returned when the product was added
        """
        return cast(JsonResponse, self._call("delete_product", {"id": id}, request_options))

    def fetch_offers(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        refresh: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Read every offer from Amazon. Reads the offers on Amazon for 1 credit, refunded if it doesn't answer. A read made in the last 3 hours, by anyone, is returned instead, for free (charged: false). The answer is the same as GET /offers.

        ``POST /offers``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
            refresh: Read Amazon again unless the last read is under 5 minutes old (1 credit)
        """
        return cast(
            JsonResponse,
            self._call(
                "fetch_offers",
                {"asin": asin, "marketplace": marketplace, "refresh": refresh},
                request_options,
            ),
        )

    def get_account(
        self,
        *,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Plan and remaining credits. Your plan, the credits left (monthly allowance and packs), how many products you track and the credits they use per month.

        ``GET /account``
        """
        return cast(JsonResponse, self._call("get_account", {}, request_options))

    def get_asin_history(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        days: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Price history of any ASIN. Every price Asin read for an ASIN on a marketplace over the period, whoever tracks it, oldest first, with the lowest, highest and average of those prices. A history of more than 5000 points is thinned evenly, keeping its first and last poi…

        ``GET /history``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
            days: History period in days
        """
        return cast(
            JsonResponse,
            self._call(
                "get_asin_history",
                {"asin": asin, "marketplace": marketplace, "days": days},
                request_options,
            ),
        )

    def get_offers(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Offers already known. Who sells the product and at what price, as last read, cheapest first, with Amazon's own price and the cheapest new and used offers (used is only known for Amazon's own outlet). Free: this never reads Amazon or spends a credit. When nobody…

        ``GET /offers``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
        """
        return cast(
            JsonResponse,
            self._call("get_offers", {"asin": asin, "marketplace": marketplace}, request_options),
        )

    def get_product(
        self,
        *,
        id: str,
        days: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Get a product and its price history. The product's latest state and every price read of the period, oldest first. The history covers every read of this ASIN on this marketplace, including those made before you added it, so a product added today can come with months of prices;…

        ``GET /products/{id}``

        Args:
            id: product_id returned when the product was added
            days: History period in days
        """
        return cast(
            JsonResponse, self._call("get_product", {"id": id, "days": days}, request_options)
        )

    def list_products(
        self,
        *,
        asin: str | None = None,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        filter: Literal["all", "drops", "target", "out_of_stock", "attention", "paused"]
        | str
        | None = None,
        page: int | None = None,
        limit: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """List tracked products. Your watchlist, newest first, with each product's latest state and its recent prices (trend). Filter with asin (and marketplace) to know if a product is tracked, or with filter to get the same lists as the app's tabs.

        ``GET /products``

        Args:
            asin: Only this ASIN
            marketplace: Only this Amazon store
            filter: Only the products of one of the app's watchlist filters. all: Every tracked product (default). drops: Cheaper now than when the product was added. target: At or below its target price. out_of_stock:…
            page: Page number
            limit: Products per page
        """
        return cast(
            JsonResponse,
            self._call(
                "list_products",
                {
                    "asin": asin,
                    "marketplace": marketplace,
                    "filter": filter,
                    "page": page,
                    "limit": limit,
                },
                request_options,
            ),
        )

    def search_amazon(
        self,
        *,
        query: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Search Amazon. Amazon search results (up to 60, sponsored included), to find the ASIN of a product. Free, limited to 30 searches per hour.

        ``GET /search``

        Args:
            query: Keywords
            marketplace: Amazon store, e.g. com for amazon.com
        """
        return cast(
            JsonResponse,
            self._call(
                "search_amazon", {"query": query, "marketplace": marketplace}, request_options
            ),
        )

    def track_product(
        self,
        *,
        product: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        target_price: int | float | None = None,
        interval_minutes: int | None = None,
        wait: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Track a product. Adds an ASIN, an Amazon link or a short link (amzn.to, a.co…) to your watchlist. The first check runs in the background within seconds (checking is true until then): poll GET /products/{id}, or send wait: true to get the answer once it's d…

        ``POST /products``

        Args:
            product: ASIN (B09DFCB66S) or Amazon product link
            marketplace: Amazon store, e.g. com for amazon.com. A product link sets it on its own.
            target_price: Email the owner when the price goes at or below this amount. null removes it.
            interval_minutes: Minutes between two checks (1440 = daily). Checks faster than daily need a plan or a credit pack: every 60 minutes with a pack or Starter, 30 with Pro, 5 with Business.
            wait: Answer once the first check is done (up to 45 seconds)
        """
        return cast(
            JsonResponse,
            self._call(
                "track_product",
                {
                    "product": product,
                    "marketplace": marketplace,
                    "target_price": target_price,
                    "interval_minutes": interval_minutes,
                    "wait": wait,
                },
                request_options,
            ),
        )

    def update_product(
        self,
        *,
        id: str,
        target_price: int | float | None = None,
        interval_minutes: int | None = None,
        alert_on_drop: bool | None = None,
        paused: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Change alerts and checks. Target price, drop alerts, check interval, or pause. Send only what changes.

        ``PATCH /products/{id}``

        Args:
            id: product_id returned when the product was added
            target_price: Email the owner when the price goes at or below this amount. null removes it.
            interval_minutes: Minutes between two checks (1440 = daily). Checks faster than daily need a plan or a credit pack: every 60 minutes with a pack or Starter, 30 with Pro, 5 with Business.
            alert_on_drop: Email when the price drops or the product is back in stock
            paused: Stop checking (and charging) for now; false resumes
        """
        return cast(
            JsonResponse,
            self._call(
                "update_product",
                {
                    "id": id,
                    "target_price": target_price,
                    "interval_minutes": interval_minutes,
                    "alert_on_drop": alert_on_drop,
                    "paused": paused,
                },
                request_options,
            ),
        )


class _AsyncOperations:
    """Generated Asin endpoint methods."""

    __slots__ = ()

    async def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        raise NotImplementedError

    async def check_product(
        self,
        *,
        id: str,
        wait: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Check the price now. Asks for a check right away (1 credit), at most once per 5 minutes; earlier calls return the product unchanged. A paused product has to be resumed first. The check runs in the background; with wait=true the answer waits for it. Read last_e…

        ``POST /products/{id}/check``

        Args:
            id: product_id returned when the product was added
            wait: Answer once the check is done (up to 45 seconds)
        """
        return cast(
            JsonResponse,
            await self._call("check_product", {"id": id, "wait": wait}, request_options),
        )

    async def delete_product(
        self,
        *,
        id: str,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Stop tracking a product. Removes the product and its price history.

        ``DELETE /products/{id}``

        Args:
            id: product_id returned when the product was added
        """
        return cast(JsonResponse, await self._call("delete_product", {"id": id}, request_options))

    async def fetch_offers(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        refresh: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Read every offer from Amazon. Reads the offers on Amazon for 1 credit, refunded if it doesn't answer. A read made in the last 3 hours, by anyone, is returned instead, for free (charged: false). The answer is the same as GET /offers.

        ``POST /offers``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
            refresh: Read Amazon again unless the last read is under 5 minutes old (1 credit)
        """
        return cast(
            JsonResponse,
            await self._call(
                "fetch_offers",
                {"asin": asin, "marketplace": marketplace, "refresh": refresh},
                request_options,
            ),
        )

    async def get_account(
        self,
        *,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Plan and remaining credits. Your plan, the credits left (monthly allowance and packs), how many products you track and the credits they use per month.

        ``GET /account``
        """
        return cast(JsonResponse, await self._call("get_account", {}, request_options))

    async def get_asin_history(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        days: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Price history of any ASIN. Every price Asin read for an ASIN on a marketplace over the period, whoever tracks it, oldest first, with the lowest, highest and average of those prices. A history of more than 5000 points is thinned evenly, keeping its first and last poi…

        ``GET /history``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
            days: History period in days
        """
        return cast(
            JsonResponse,
            await self._call(
                "get_asin_history",
                {"asin": asin, "marketplace": marketplace, "days": days},
                request_options,
            ),
        )

    async def get_offers(
        self,
        *,
        asin: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Offers already known. Who sells the product and at what price, as last read, cheapest first, with Amazon's own price and the cheapest new and used offers (used is only known for Amazon's own outlet). Free: this never reads Amazon or spends a credit. When nobody…

        ``GET /offers``

        Args:
            asin: 10-character ASIN
            marketplace: Amazon store, e.g. com for amazon.com
        """
        return cast(
            JsonResponse,
            await self._call(
                "get_offers", {"asin": asin, "marketplace": marketplace}, request_options
            ),
        )

    async def get_product(
        self,
        *,
        id: str,
        days: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Get a product and its price history. The product's latest state and every price read of the period, oldest first. The history covers every read of this ASIN on this marketplace, including those made before you added it, so a product added today can come with months of prices;…

        ``GET /products/{id}``

        Args:
            id: product_id returned when the product was added
            days: History period in days
        """
        return cast(
            JsonResponse, await self._call("get_product", {"id": id, "days": days}, request_options)
        )

    async def list_products(
        self,
        *,
        asin: str | None = None,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        filter: Literal["all", "drops", "target", "out_of_stock", "attention", "paused"]
        | str
        | None = None,
        page: int | None = None,
        limit: int | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """List tracked products. Your watchlist, newest first, with each product's latest state and its recent prices (trend). Filter with asin (and marketplace) to know if a product is tracked, or with filter to get the same lists as the app's tabs.

        ``GET /products``

        Args:
            asin: Only this ASIN
            marketplace: Only this Amazon store
            filter: Only the products of one of the app's watchlist filters. all: Every tracked product (default). drops: Cheaper now than when the product was added. target: At or below its target price. out_of_stock:…
            page: Page number
            limit: Products per page
        """
        return cast(
            JsonResponse,
            await self._call(
                "list_products",
                {
                    "asin": asin,
                    "marketplace": marketplace,
                    "filter": filter,
                    "page": page,
                    "limit": limit,
                },
                request_options,
            ),
        )

    async def search_amazon(
        self,
        *,
        query: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Search Amazon. Amazon search results (up to 60, sponsored included), to find the ASIN of a product. Free, limited to 30 searches per hour.

        ``GET /search``

        Args:
            query: Keywords
            marketplace: Amazon store, e.g. com for amazon.com
        """
        return cast(
            JsonResponse,
            await self._call(
                "search_amazon", {"query": query, "marketplace": marketplace}, request_options
            ),
        )

    async def track_product(
        self,
        *,
        product: str,
        marketplace: Literal[
            "com", "co.uk", "de", "fr", "it", "es", "ca", "co.jp", "com.br", "com.mx", "in"
        ]
        | str
        | None = None,
        target_price: int | float | None = None,
        interval_minutes: int | None = None,
        wait: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Track a product. Adds an ASIN, an Amazon link or a short link (amzn.to, a.co…) to your watchlist. The first check runs in the background within seconds (checking is true until then): poll GET /products/{id}, or send wait: true to get the answer once it's d…

        ``POST /products``

        Args:
            product: ASIN (B09DFCB66S) or Amazon product link
            marketplace: Amazon store, e.g. com for amazon.com. A product link sets it on its own.
            target_price: Email the owner when the price goes at or below this amount. null removes it.
            interval_minutes: Minutes between two checks (1440 = daily). Checks faster than daily need a plan or a credit pack: every 60 minutes with a pack or Starter, 30 with Pro, 5 with Business.
            wait: Answer once the first check is done (up to 45 seconds)
        """
        return cast(
            JsonResponse,
            await self._call(
                "track_product",
                {
                    "product": product,
                    "marketplace": marketplace,
                    "target_price": target_price,
                    "interval_minutes": interval_minutes,
                    "wait": wait,
                },
                request_options,
            ),
        )

    async def update_product(
        self,
        *,
        id: str,
        target_price: int | float | None = None,
        interval_minutes: int | None = None,
        alert_on_drop: bool | None = None,
        paused: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Change alerts and checks. Target price, drop alerts, check interval, or pause. Send only what changes.

        ``PATCH /products/{id}``

        Args:
            id: product_id returned when the product was added
            target_price: Email the owner when the price goes at or below this amount. null removes it.
            interval_minutes: Minutes between two checks (1440 = daily). Checks faster than daily need a plan or a credit pack: every 60 minutes with a pack or Starter, 30 with Pro, 5 with Business.
            alert_on_drop: Email when the price drops or the product is back in stock
            paused: Stop checking (and charging) for now; false resumes
        """
        return cast(
            JsonResponse,
            await self._call(
                "update_product",
                {
                    "id": id,
                    "target_price": target_price,
                    "interval_minutes": interval_minutes,
                    "alert_on_drop": alert_on_drop,
                    "paused": paused,
                },
                request_options,
            ),
        )
