# _client.py
from __future__ import annotations

import os

from .resources import Recommender, AnamolyDetector, DataConnector
from ._exceptions import PigeonsAIError


__all__ = [
    "PigeonsAI",
]


class PigeonsAI():
    recommender: Recommender
    anamoly_detector: AnamolyDetector
    data_connector: DataConnector

    # client options
    api_key: str

    def __init__(
        self,
        api_key: str | None = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("PIGEONSAI_API_KEY")
        if api_key is None:
            raise PigeonsAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the PIGEONSAI_API_KEY environment variable"
            )
        self.api_key = api_key

        self.recommender = Recommender(self)
        self.anamoly_detector = AnamolyDetector()
        self.data_connector = DataConnector(self)

    @property
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key

        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key
        }

        return headers
