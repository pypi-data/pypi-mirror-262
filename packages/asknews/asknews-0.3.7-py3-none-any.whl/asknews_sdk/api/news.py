from datetime import datetime
from typing import Literal

from asknews_sdk.api.base import BaseAPI
from asknews_sdk.dto.news import (
    SearchResponse,
    AnalyticsResponse,
    WordCloudResponse,
    SummariesResponse,
)


class NewsAPI(BaseAPI):
    """
    News API

    https://api.asknews.app/docs#tag/news
    """
    async def get_news_analytics(
        self,
        return_pct: bool = False,
        sentiment_type: str = "total_sentiment",
        hours_back: int = 24,
        smoothing: int = 1,
        candidates: list[str] | None = None,
    ) -> AnalyticsResponse:
        """
        Get the precomputed analytics from the news given the parameters.

        https://api.asknews.app/docs#/news/operation/get_news_analytics
        """
        response = await self.client.get(
            endpoint="/v1/news/analytics",
            query={
                "return_pct": return_pct,
                "sentiment_type": sentiment_type,
                "hours_back": hours_back,
                "smoothing": smoothing,
                "candidates": candidates,
            },
            accept=[(AnalyticsResponse.__content_type__, 1.0)]
        )
        return AnalyticsResponse.model_validate(response.content)

    async def get_news_wordcloud(
        self,
        sentiment_type: str = "total_sentiment",
        hours_back: int = 24,
        candidates: list[str] | None = None,
    ) -> WordCloudResponse:
        """
        Get the precomputed wordcloud from the news given the parameters.

        https://api.asknews.app/docs#/news/operation/get_news_wordcloud
        """
        response = await self.client.get(
            endpoint="/v1/news/wordcloud",
            query={
                "sentiment_type": sentiment_type,
                "hours_back": hours_back,
                "candidates": candidates,
            },
            accept=[(WordCloudResponse.__content_type__, 1.0)]
        )
        return WordCloudResponse.model_validate(response.content)

    async def get_news_summaries(
        self,
        start: int = 0,
        stop: int = 0,
        candidates: list[str] | None = None,
    ) -> SummariesResponse:
        """
        Get the precomputed summaries from the news given the parameters.

        https://api.asknews.app/docs#/news/operation/get_news_summaries
        """
        response = await self.client.get(
            endpoint="/v1/news/summaries",
            query={
                "start": start,
                "stop": stop,
                "candidates": candidates,
            },
            accept=[(SummariesResponse.__content_type__, 1.0)]  # type: ignore
        )
        return SummariesResponse.model_validate(response.content)

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
