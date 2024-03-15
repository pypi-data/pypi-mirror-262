from __future__ import annotations

from typing import Annotated
from datetime import datetime
from pydantic import AnyUrl, BaseModel, Field, RootModel

from asknews_sdk.dto.base import BaseSchema


class AnalyticsResponseCandidateInfo(BaseModel):
    time_stamps: Annotated[list[datetime], Field(title='Time Stamps')]
    sentiment: Annotated[list[float], Field(title='Sentiment')]
    total_sentiment: Annotated[list[float], Field(title='Total Sentiment')]
    color_id: Annotated[str, Field(title='Color Id')]


class AnalyticsResponseNewsCount(BaseModel):
    time_stamps: Annotated[list[datetime], Field(title='Time Stamps')]
    news_count: Annotated[list[int], Field(title='News Count')]
    color_id: Annotated[str, Field(title='Color Id')]


class AnalyticsResponsePartyInfo(BaseModel):
    time_stamps: Annotated[list[datetime], Field(title='Time Stamps')]
    sentiment: Annotated[list[float], Field(title='Sentiment')]
    total_sentiment: Annotated[list[float], Field(title='Total Sentiment')]
    color_id: Annotated[str, Field(title='Color Id')]


class AnalyticsResponse(BaseSchema):
    candidates: Annotated[
        dict[str, AnalyticsResponseCandidateInfo], Field(title='Candidates')
    ]
    parties: Annotated[dict[str, AnalyticsResponsePartyInfo], Field(title='Parties')]
    news_count: AnalyticsResponseNewsCount


class SummariesResponseItemCandidateInfo(BaseModel):
    mentioned: Annotated[bool, Field(title='Mentioned')]
    reason: Annotated[str, Field(title='Reason')]
    role: Annotated[str, Field(title='Role')]
    sentiment: Annotated[int, Field(title='Sentiment')]


class SummariesResponseItemPartyInfo(BaseModel):
    mentioned: Annotated[bool, Field(title='Mentioned')]
    reason: Annotated[str, Field(title='Reason')]
    sentiment: Annotated[int, Field(title='Sentiment')]


class SummariesResponseItemAnalysis(BaseModel):
    candidates: Annotated[
        dict[str, SummariesResponseItemCandidateInfo], Field(title='Candidates')
    ]
    parties: Annotated[
        dict[str, SummariesResponseItemPartyInfo], Field(title='Parties')
    ]
    classification: Annotated[list[str], Field(title='Classification')]
    keywords: Annotated[list[str], Field(title='Keywords')]
    sentiment: Annotated[int, Field(title='Sentiment')]
    source: Annotated[str, Field(title='Source')]
    summary: Annotated[str, Field(title='Summary')]
    title: Annotated[str, Field(title='Title')]


class SummariesResponseItem(BaseModel):
    analysis: SummariesResponseItemAnalysis
    candidate: Annotated[list[str], Field(title='Candidate')]
    timestamp: Annotated[int, Field(title='Timestamp')]
    article_url: Annotated[AnyUrl, Field(title='Article Url')]


class SummariesResponse(RootModel[list[SummariesResponseItem]]):
    root: Annotated[list[SummariesResponseItem], Field(title='SummariesResponse')]


class SearchResponseDictItemEntites(BaseModel):
    CARDINAL: Annotated[list[str] | None, Field(title='Cardinal')] = None
    DATE: Annotated[list[str] | None, Field(title='Date')] = None
    GPE: Annotated[list[str] | None, Field(title='Gpe')] = None
    ORG: Annotated[list[str] | None, Field(title='Org')] = None
    PERSON: Annotated[list[str] | None, Field(title='Person')] = None


class SearchResponseDictItem(BaseModel):
    as_string_key: Annotated[str, Field(title='As String Key')]
    summary: Annotated[str, Field(title='Summary')]
    article_id: Annotated[str, Field(title='Article Id')]
    content: Annotated[str, Field(title='Content')]
    country: Annotated[str, Field(title='Country')]
    image_url: Annotated[AnyUrl, Field(title='Image Url')]
    entities: SearchResponseDictItemEntites
    link: Annotated[AnyUrl, Field(title='Link')]
    pubDate: Annotated[datetime, Field(title='Pubdate')]
    rank: Annotated[int, Field(title='Rank')]
    eng_title: Annotated[str, Field(title='Eng Title')]
    title: Annotated[str, Field(title='Title')]
    name_source: Annotated[str | None, Field(title='Name Source')] = "Unknown"


class SearchResponse(BaseSchema):
    as_dicts: Annotated[
        list[SearchResponseDictItem] | None, Field(title='As Dicts')
    ] = None
    as_string: Annotated[str | None, Field(title='As String')] = None


class WordCloudResponseItem(BaseModel):
    text: Annotated[str, Field(title='Text')]
    value: Annotated[int, Field(title='Value')]


class WordCloudResponse(BaseSchema):
    news_sources: Annotated[list[WordCloudResponseItem], Field(title='News Sources')]
