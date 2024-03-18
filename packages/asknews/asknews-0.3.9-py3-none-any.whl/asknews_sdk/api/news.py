from datetime import datetime
from typing import Literal

from asknews_sdk.api.base import BaseAPI
from asknews_sdk.dto.news import (
    SearchResponse
)


class NewsAPI(BaseAPI):
    """
    News API

    https://api.asknews.app/docs#tag/news
    """
    async def search_news(
        self,
        query: str,
        n_articles: int = 10,
        start_timestamp: int | datetime | None = None,
        end_timestamp: int | datetime | None = None,
        return_type: Literal["dicts", "string", "both"] = "dicts",
        method: Literal["nl", "kw"] = "nl",
        historical: bool = False
    ) -> SearchResponse:
        """
        Search for news articles given a query.

        https://api.asknews.app/docs#/news/operation/search_news
        """
        response = await self.client.get(
            endpoint="/v1/news/search",
            query={
                "query": query,
                "n_articles": n_articles,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "return_type": return_type,
                "method": method,
                "historical": historical
            },
            accept=[(SearchResponse.__content_type__, 1.0)]
        )
        return SearchResponse.model_validate(response.content)
