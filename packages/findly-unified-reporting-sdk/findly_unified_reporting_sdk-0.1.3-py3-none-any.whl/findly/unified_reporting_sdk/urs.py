from findly.unified_reporting_sdk.common.analytics_client import AnalyticsClient
import logging
import pandas as pd
from typing import List, Tuple, Optional

from findly.unified_reporting_sdk.protos.semantic_layer_pb2 import (
    Dimension,
    Metric,
    QueryArgs,
    DataSourceIntegration
)
from findly.unified_reporting_sdk.fb_ads.fb_ads_client import FbAdsClient
from findly.unified_reporting_sdk.ga4.ga4_client import GA4Client


class Urs(AnalyticsClient):
    """
    Attributes:
        _client(AnalyticsClient)
    """

    _client: AnalyticsClient

    def __init__(self, client_id: str, client_secret: str, token: str, integration: DataSourceIntegration.ValueType):
        ConcreteClientClass = { # noqa
            DataSourceIntegration.FB_ADS: FbAdsClient,
            DataSourceIntegration.GA4: GA4Client
        }.get(integration)

        if ConcreteClientClass is None:
            raise ValueError("Integration not supported")

        self._client = ConcreteClientClass(token=token, client_id=client_id, client_secret=client_secret)

    async def query(
        self,
        query_args: QueryArgs,
        property_id: str,
        logger: logging.LoggerAdapter,
    ) -> Optional[Tuple[List[pd.DataFrame], List[pd.DataFrame]]]:
        return await self._client.query(
            query_args=query_args,
            property_id=property_id,
            logger=logger,
        )

    async def list_property_ids(self) -> Optional[List[str]] :
        return await self._client.list_property_ids()

    async def get_dimension_values(self, dimension: Dimension, top_n: int, property_id: str) -> Optional[List[str]]:
        return await self._client.get_dimension_values(dimension=dimension, top_n=top_n, property_id=property_id)

    async def list_dimensions(self, property_id: str) -> Optional[List[Dimension]]:
        return await self._client.list_dimensions(property_id=property_id)

    async def list_metrics(self, property_id: str) -> Optional[List[Metric]]:
        return await self._client.list_metrics(property_id=property_id)

    async def get_dimension_from_name(self, dimension_name: str, property_id: str) -> Optional[Dimension]:
        return await self._client.get_dimension_from_name(dimension_name=dimension_name, property_id=property_id)

    async def get_metric_from_name(self, metric_name: str, property_id: str) -> Optional[Metric]:
        return await self._client.get_metric_from_name(metric_name=metric_name, property_id=property_id)
