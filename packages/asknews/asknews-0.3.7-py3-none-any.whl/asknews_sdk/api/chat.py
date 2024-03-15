from typing import AsyncIterator

from asknews_sdk.api.base import BaseAPI
from asknews_sdk.dto.chat import (
    CreateChatCompletionRequest,
    CreateChatCompletionResponse,
    CreateChatCompletionResponseStream,
)


class ChatAPI(BaseAPI):
    """
    Chat API

    https://api.asknews.app/docs#tag/chat
    """
    async def get_chat_completions(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-3.5-turbo-16k",
        temperature: float = 0.9,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: list[str] | None = None,
        max_tokens: int = 9999,
        presence_penalty: int = 0,
        frequency_penalty: int = 0,
        user: str = "anonymous"
    ) -> CreateChatCompletionResponse | AsyncIterator[CreateChatCompletionResponseStream]:
        """
        Get chat completions for a given user message.

        https://api.asknews.app/docs#tag/chat/operation/get_chat_completions
        """
        response = await self.client.post(
            endpoint="/v1/chat/completions",
            body=CreateChatCompletionRequest(
                messages=messages,
                model=model,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                stop=stop,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                user=user
            ).model_dump(mode="json"),
            headers={
                "Content-Type": CreateChatCompletionRequest.__content_type__,
            },
            accept=[
                (CreateChatCompletionResponse.__content_type__, 1.0),
                (CreateChatCompletionResponseStream.__content_type__, 1.0),
            ],
            stream=stream,
            stream_type="lines"  # type: ignore
        )

        if stream:
            async def _stream():
                async for chunk in response.content:
                    if chunk.strip() == "data: [DONE]":
                        break

                    if chunk.startswith("data:"):
                        json_data = chunk.replace("data: ", "").strip()
                        yield CreateChatCompletionResponseStream.model_validate_json(json_data)
            return _stream()
        else:
            return CreateChatCompletionResponse.model_validate(response.content)

    async def get_headline_questions(
        self,
        queries: list[str] | None = None
    ) -> dict[str, list[str]]:
        """
        Get headline questions for a given query.

        https://api.asknews.app/docs#tag/chat/operation/get_headline_questions
        """
        response = await self.client.get(
            endpoint="/v1/chat/questions",
            query={"queries": queries}
        )
        return response.content
