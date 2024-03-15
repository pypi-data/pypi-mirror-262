from datetime import datetime

from asknews_sdk.api.base import BaseAPI
from asknews_sdk.dto.sentiment import SentimentResponse


class SentimentAPI(BaseAPI):
    """
    Sentiment API

    https://api.asknews.app/docs#/sentiment
    """
    async def get_coin_sentiment(
        self,
        slug: str,
        metric: str,
        date_from: str | datetime,
        date_to: str | datetime,
    ) -> SentimentResponse:
        """
        Get the timeseries sentiment for a coin.

        https://docs.asknews.app/#/sentiment/get_coin_sentiment

        :param slug: The coin slug.
        :type slug: str
        :param metric: The sentiment metric.
        :type metric: str
        :param date_from: The start date in ISO format.
        :type date_from: str | datetime
        :param date_to: The end date in ISO format.
        :type date_to: str | datetime
        :return: The sentiment response.
        :rtype: SentimentResponse
        """
        response = await self.client.get(
            endpoint="/v1/sentiment",
            query={
                "slug": slug,
                "metric": metric,
                "date_from": date_from,
                "date_to": date_to
            },
            accept=[(SentimentResponse.__content_type__, 1.0)]
        )
        return SentimentResponse.model_validate(response.content)
