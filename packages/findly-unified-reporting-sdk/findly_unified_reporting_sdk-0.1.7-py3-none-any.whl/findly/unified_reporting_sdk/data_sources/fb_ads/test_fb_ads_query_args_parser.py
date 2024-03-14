import logging
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from facebook_business.api import Cursor
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.adobjects.adsinsights import AdsInsights
from findly.unified_reporting_sdk.data_sources.fb_ads.fb_ads_query_args_parser import (
    FbAdsQueryArgsParser,
    RESERVED_TOTAL,
)
from findly.unified_reporting_sdk.protos.findly_semantic_layer_pb2 import QueryArgs
import json

FB_PARSER = FbAdsQueryArgsParser.default()
LOGGER = logging.LoggerAdapter(logging.getLogger("test"), extra={})
WORKSPACE = "test_workspace"


@pytest.mark.asyncio
async def test_parse_totals_empty() -> None:
    sql_parts = QueryArgs()
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=None,
        query_args=sql_parts,
        logger=LOGGER,
    )

    # Empty dataframe list.
    assert result[0].equals(pd.DataFrame([]))


@pytest.mark.asyncio
async def test_parse_totals_no_dimensions() -> None:
    sql_parts = QueryArgs(
        metrics=["clicks", "impressions"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
        <Summary> {
            "clicks": "249724",
            "date_start": "2023-02-06",
            "date_stop": "2024-02-06",
            "impressions": "17075028"
        }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame({"clicks": ["249724"], "impressions": ["17075028"]})

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_totals_no_metrics() -> None:
    sql_parts = QueryArgs(
        metrics=[],
        group_by_columns=["campaign_name"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "date_start": "2023-02-06",
        "date_stop": "2024-02-06"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame({"campaign_name": [RESERVED_TOTAL]})

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_simple_totals() -> None:
    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["gender"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "date_start": "2023-02-06",
        "date_stop": "2024-02-06",
        "impressions": "17075028"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {"impressions": ["17075028"], "gender": [RESERVED_TOTAL]}
    )

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_simple_action_totals() -> None:
    sql_parts = QueryArgs(
        metrics=["actions"],
        group_by_columns=["action_type"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "actions": [
            {
                "action_type": "onsite_conversion.post_save",
                "value": "1949"
            },
            {
                "action_type": "onsite_conversion.view_content",
                "value": "85"
            },
            {
                "action_type": "onsite_conversion.add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "post",
                "value": "926"
            },
            {
                "action_type": "onsite_web_app_view_content",
                "value": "46347"
            },
            {
                "action_type": "landing_page_view",
                "value": "113341"
            },
            {
                "action_type": "omni_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_app_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "comment",
                "value": "2245"
            },
            {
                "action_type": "onsite_web_app_purchase",
                "value": "8473"
            },
            {
                "action_type": "page_engagement",
                "value": "2949722"
            },
            {
                "action_type": "purchase",
                "value": "8473"
            },
            {
                "action_type": "post_engagement",
                "value": "2949707"
            },
            {
                "action_type": "onsite_web_purchase",
                "value": "8473"
            },
            {
                "action_type": "view_content",
                "value": "46262"
            },
            {
                "action_type": "onsite_app_view_content",
                "value": "85"
            },
            {
                "action_type": "add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "like",
                "value": "15"
            },
            {
                "action_type": "onsite_web_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_view_content",
                "value": "46347"
            },
            {
                "action_type": "video_view",
                "value": "2774220"
            },
            {
                "action_type": "omni_view_content",
                "value": "46347"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_view_content",
                "value": "46262"
            },
            {
                "action_type": "post_reaction",
                "value": "20071"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_purchase",
                "value": "8473"
            },
            {
                "action_type": "omni_add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "link_click",
                "value": "150296"
            },
            {
                "action_type": "omni_purchase",
                "value": "847"
            }
        ],
        "date_start": "2023-02-06",
        "date_stop": "2024-02-06"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )
    expected_result = pd.DataFrame(
        {"action_type": [RESERVED_TOTAL], "actions": ["10188238"]}
    )

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_complex_action_totals_1() -> None:
    sql_parts = QueryArgs(
        metrics=["actions", "impressions"],
        group_by_columns=["action_type", "gender"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "actions": [
            {
                "action_type": "onsite_conversion.post_save",
                "value": "1949"
            },
            {
                "action_type": "onsite_conversion.view_content",
                "value": "85"
            },
            {
                "action_type": "onsite_conversion.add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "post",
                "value": "926"
            },
            {
                "action_type": "onsite_web_app_view_content",
                "value": "46347"
            },
            {
                "action_type": "landing_page_view",
                "value": "113341"
            },
            {
                "action_type": "omni_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_app_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "comment",
                "value": "2245"
            },
            {
                "action_type": "onsite_web_app_purchase",
                "value": "8473"
            },
            {
                "action_type": "page_engagement",
                "value": "2949722"
            },
            {
                "action_type": "purchase",
                "value": "8473"
            },
            {
                "action_type": "post_engagement",
                "value": "2949707"
            },
            {
                "action_type": "onsite_web_purchase",
                "value": "8473"
            },
            {
                "action_type": "view_content",
                "value": "46262"
            },
            {
                "action_type": "onsite_app_view_content",
                "value": "85"
            },
            {
                "action_type": "add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "like",
                "value": "15"
            },
            {
                "action_type": "onsite_web_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_view_content",
                "value": "46347"
            },
            {
                "action_type": "video_view",
                "value": "2774220"
            },
            {
                "action_type": "omni_view_content",
                "value": "46347"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_view_content",
                "value": "46262"
            },
            {
                "action_type": "post_reaction",
                "value": "20071"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_purchase",
                "value": "8473"
            },
            {
                "action_type": "omni_add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "link_click",
                "value": "150296"
            },
            {
                "action_type": "omni_purchase",
                "value": "8473"
            }
        ],
        "date_start": "2023-02-06",
        "date_stop": "2024-02-06",
        "impressions": "17075028"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "impressions": ["17075028"],
            "action_type": [RESERVED_TOTAL],
            "actions": ["10195864"],
            "gender": [RESERVED_TOTAL],
        }
    )

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_complex_action_totals_2() -> None:
    sql_parts = QueryArgs(
        metrics=[
            "clicks",
            "cpc",
            "cpm",
            "cpp",
            "ctr",
            "impressions",
            "reach",
            "spend",
            "cost_per_ad_click",
            "actions",
        ],
        group_by_columns=["action_type"],
        date_ranges="(2023-02-06, 2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "actions": [
            {
                "action_type": "onsite_conversion.post_save",
                "value": "807"
            },
            {
                "action_type": "onsite_conversion.view_content",
                "value": "47"
            },
            {
                "action_type": "onsite_conversion.add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "post",
                "value": "395"
            },
            {
                "action_type": "onsite_web_app_view_content",
                "value": "20571"
            },
            {
                "action_type": "landing_page_view",
                "value": "42096"
            },
            {
                "action_type": "omni_add_to_cart",
                "value": "69890"
            },
            {
                "action_type": "onsite_web_app_add_to_cart",
                "value": "69890"
            },
            {
                "action_type": "comment",
                "value": "1054"
            },
            {
                "action_type": "onsite_web_app_purchase",
                "value": "4080"
            },
            {
                "action_type": "page_engagement",
                "value": "1008628"
            },
            {
                "action_type": "purchase",
                "value": "4080"
            },
            {
                "action_type": "post_engagement",
                "value": "1008622"
            },
            {
                "action_type": "onsite_web_purchase",
                "value": "4080"
            },
            {
                "action_type": "view_content",
                "value": "20524"
            },
            {
                "action_type": "onsite_app_view_content",
                "value": "47"
            },
            {
                "action_type": "add_to_cart",
                "value": "69890"
            },
            {
                "action_type": "like",
                "value": "6"
            },
            {
                "action_type": "onsite_web_add_to_cart",
                "value": "69890"
            },
            {
                "action_type": "onsite_web_view_content",
                "value": "20571"
            },
            {
                "action_type": "video_view",
                "value": "939594"
            },
            {
                "action_type": "omni_view_content",
                "value": "20571"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_view_content",
                "value": "20524"
            },
            {
                "action_type": "post_reaction",
                "value": "7220"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                "value": "69890"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_purchase",
                "value": "4080"
            },
            {
                "action_type": "omni_add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "link_click",
                "value": "59552"
            },
            {
                "action_type": "omni_purchase",
                "value": "4080"
            }
        ],
        "clicks": "97848",
        "cpc": "0.919213",
        "cpm": "14.246652",
        "cpp": "55.649409",
        "ctr": "1.549874",
        "date_start": "2023-12-01",
        "date_stop": "2023-12-31",
        "impressions": "6313286",
        "reach": "1616247",
        "spend": "89943.19"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "clicks": ["97848"],
            "cpc": ["0.92"],
            "cpm": ["14.25"],
            "cpp": ["55.65"],
            "ctr": ["1.55"],
            "impressions": ["6313286"],
            "reach": ["1616247"],
            "spend": ["89943.19"],
            "cost_per_ad_click": np.nan,
            "action_type": [RESERVED_TOTAL],
            "actions": ["3540681"],
        }
    )
    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_double_action_totals() -> None:
    sql_parts = QueryArgs(
        metrics=["actions", "action_values"],
        group_by_columns=["action_type"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)

    summary_text = """
    <Summary> {
        "action_values": [
            {
                "action_type": "onsite_web_app_purchase",
                "value": "545445.05"
            },
            {
                "action_type": "omni_purchase",
                "value": "545445.05"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_purchase",
                "value": "545445.05"
            },
            {
                "action_type": "purchase",
                "value": "545445.05"
            },
            {
                "action_type": "onsite_web_purchase",
                "value": "545445.05"
            }
        ],
        "actions": [
            {
                "action_type": "onsite_conversion.post_save",
                "value": "1949"
            },
            {
                "action_type": "onsite_conversion.view_content",
                "value": "85"
            },
            {
                "action_type": "onsite_conversion.add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "post",
                "value": "926"
            },
            {
                "action_type": "onsite_web_app_view_content",
                "value": "46347"
            },
            {
                "action_type": "landing_page_view",
                "value": "113341"
            },
            {
                "action_type": "omni_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_app_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "comment",
                "value": "2245"
            },
            {
                "action_type": "onsite_web_app_purchase",
                "value": "8473"
            },
            {
                "action_type": "page_engagement",
                "value": "2949722"
            },
            {
                "action_type": "purchase",
                "value": "8473"
            },
            {
                "action_type": "post_engagement",
                "value": "2949707"
            },
            {
                "action_type": "onsite_web_purchase",
                "value": "8473"
            },
            {
                "action_type": "view_content",
                "value": "46262"
            },
            {
                "action_type": "onsite_app_view_content",
                "value": "85"
            },
            {
                "action_type": "add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "like",
                "value": "15"
            },
            {
                "action_type": "onsite_web_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "onsite_web_view_content",
                "value": "46347"
            },
            {
                "action_type": "video_view",
                "value": "2774220"
            },
            {
                "action_type": "omni_view_content",
                "value": "46347"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_view_content",
                "value": "46262"
            },
            {
                "action_type": "post_reaction",
                "value": "20071"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                "value": "191854"
            },
            {
                "action_type": "offsite_conversion.fb_pixel_purchase",
                "value": "8473"
            },
            {
                "action_type": "omni_add_to_wishlist",
                "value": "1"
            },
            {
                "action_type": "link_click",
                "value": "150296"
            },
            {
                "action_type": "omni_purchase",
                "value": "8473"
            }
        ],
        "date_start": "2023-02-06",
        "date_stop": "2024-02-06"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text
    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "action_type": [RESERVED_TOTAL],
            "action_values": ["2727225.25"],
            "actions": ["10195864"],
        }
    )

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_multiple_date_ranges_totals() -> None:
    # Unlike in ga4, fb will output just one total for all date ranges
    # starting in the oldest date and ending in the newest date
    # It will output like that even if the date ranges are not continuous

    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["impression_device"],
        date_ranges="(2023-10-01,2023-10-31), (2023-12-01,2023-12-31)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock Cursor to return summary data as a string
    mock_cursor = MagicMock(spec=Cursor)
    summary_text = """
    <Summary> {
        "date_start": "2023-10-01",
        "date_stop": "2023-12-31",
        "impressions": "8303278"
    }
    """
    summary_json = summary_text.split("> ")[1]
    summary = json.loads(summary_json)

    mock_cursor.summary.return_value = summary_text

    result = FB_PARSER.parse_totals_to_dataframe(
        summary=summary,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "impressions": ["8303278"],
            "impression_device": [RESERVED_TOTAL],
        }
    )

    # Check if the result matches the expected dataframe
    assert result[0].equals(expected_result)

@pytest.mark.asyncio
async def test_parse_report_response_empty() -> None:
    sql_parts = QueryArgs()
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Mock the Cursor to return the AdsInsights objects
    report_response = Cursor(
        source_object=mock_ad_report_run, target_objects_class=AdsInsights
    )
    report_response._queue = []
    report_response.load_next_page = MagicMock(
        return_value=False
    )  # Ensure no more pages are loaded

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=[],
        query_args=sql_parts,
        logger=LOGGER,
    )
    expected_result = pd.DataFrame({})

    # Check if the result dataframe matches the expected dataframe
    assert result[0].equals(expected_result)


@pytest.mark.asyncio
async def test_parse_report_response_no_dimensions() -> None:
    sql_parts = QueryArgs(
        metrics=["clicks", "impressions"],
        date_ranges="(2023-12-01,2023-12-31)",
        level=AdsInsights.Level.account,
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    ads_insight_data = {
        "clicks": "97848",
        "date_start": "2023-12-01",
        "date_stop": "2023-12-31",
        "impressions": "6313286",
    }
    ads_insight = AdsInsights()
    ads_insight.set_data(ads_insight_data)

    report_response = [ads_insight]

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame({"clicks": ["97848"], "impressions": ["6313286"]})

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_no_metric() -> None:
    sql_parts = QueryArgs(
        metrics=[],
        group_by_columns=["campaign_name"],
        date_ranges="(2023-12-01,2023-12-31)",
        level=AdsInsights.Level.campaign,
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.AQUA-HORSE-15112023___d.BTH-RT-7-DAYS___p.BTH__l.EN-US__f.BOF",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.AQUA-DONKEY-15112023___d.BTH-RT-14-DAYS___p.BTH__l.EN-US__f.BOF",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.AQUA-MOOSE-15112023___d.BTH-RT-30-DAYS___p.BTH__l.EN-US__f.BOF",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.AQUA-DEER-15112023___d.BTH-RT-30+-DAYS___p.BTH__l.EN-US__f.BOF",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.LIME-TIGER-16112023___d.BTH-RT-REPEAT-BUYERS-30-DAYS___p.BTH__l.EN-US",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.LIME-KANGAROO-16112023___d.BTH-RT-REPEAT-BUYERS-60-DAYS___p.BTH__l.EN-US",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
        {
            "campaign_name": "c.FBP__s.BAERSKIN__i.LIME-DUCK-16112023___d.BTH-RT-REPEAT-BUYERS-2-YEARS___p.BTH__l.EN-US",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "campaign_name": [
                "c.FBP__s.BAERSKIN__i.AQUA-HORSE-15112023___d.BTH-RT-7-DAYS___p.BTH__l.EN-US__f.BOF",
                "c.FBP__s.BAERSKIN__i.AQUA-DONKEY-15112023___d.BTH-RT-14-DAYS___p.BTH__l.EN-US__f.BOF",
                "c.FBP__s.BAERSKIN__i.AQUA-MOOSE-15112023___d.BTH-RT-30-DAYS___p.BTH__l.EN-US__f.BOF",
                "c.FBP__s.BAERSKIN__i.AQUA-DEER-15112023___d.BTH-RT-30+-DAYS___p.BTH__l.EN-US__f.BOF",
                "c.FBP__s.BAERSKIN__i.LIME-TIGER-16112023___d.BTH-RT-REPEAT-BUYERS-30-DAYS___p.BTH__l.EN-US",
                "c.FBP__s.BAERSKIN__i.LIME-KANGAROO-16112023___d.BTH-RT-REPEAT-BUYERS-60-DAYS___p.BTH__l.EN-US",
                "c.FBP__s.BAERSKIN__i.LIME-DUCK-16112023___d.BTH-RT-REPEAT-BUYERS-2-YEARS___p.BTH__l.EN-US",
            ]
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_simple() -> None:
    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["gender"],
        date_ranges="(2023-12-01,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "female",
            "impressions": "1861808",
        },
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "male",
            "impressions": "4359639",
        },
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "unknown",
            "impressions": "91839",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "gender": ["female", "male", "unknown"],
            "impressions": ["1861808", "4359639", "91839"],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_missing_data() -> None:
    sql_parts = QueryArgs(
        metrics=["conversions"],
        group_by_columns=["gender"],
        date_ranges="(2023-12-01,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {"date_start": "2023-12-01", "date_stop": "2023-12-31", "gender": "female"},
        {"date_start": "2023-12-01", "date_stop": "2023-12-31", "gender": "male"},
        {"date_start": "2023-12-01", "date_stop": "2023-12-31", "gender": "unknown"},
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "gender": ["female", "male", "unknown"],
            "conversions": [np.nan, np.nan, np.nan],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_date_dimension() -> None:
    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["date"],
        date_ranges="(2023-12-29,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "date_start": "2023-12-29",
            "date_stop": "2023-12-29",
            "impressions": "195993",
        },
        {
            "date_start": "2023-12-30",
            "date_stop": "2023-12-30",
            "impressions": "200868",
        },
        {
            "date_start": "2023-12-31",
            "date_stop": "2023-12-31",
            "impressions": "209774",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "date": ["2023-12-29", "2023-12-30", "2023-12-31"],
            "impressions": ["195993", "200868", "209774"],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_simple_action() -> None:
    sql_parts = QueryArgs(
        metrics=["actions"],
        group_by_columns=["action_type"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "actions": [
                {"action_type": "onsite_conversion.post_save", "value": "807"},
                {"action_type": "onsite_conversion.view_content", "value": "47"},
                {"action_type": "onsite_conversion.add_to_wishlist", "value": "1"},
                {"action_type": "post", "value": "395"},
                {"action_type": "onsite_web_app_view_content", "value": "20571"},
                {"action_type": "landing_page_view", "value": "42096"},
                {"action_type": "omni_add_to_cart", "value": "69890"},
                {"action_type": "onsite_web_app_add_to_cart", "value": "69890"},
                {"action_type": "comment", "value": "1054"},
                {"action_type": "onsite_web_app_purchase", "value": "4080"},
                {"action_type": "page_engagement", "value": "1008628"},
                {"action_type": "purchase", "value": "4080"},
                {"action_type": "post_engagement", "value": "1008622"},
                {"action_type": "onsite_web_purchase", "value": "4080"},
                {"action_type": "view_content", "value": "20524"},
                {"action_type": "onsite_app_view_content", "value": "47"},
                {"action_type": "add_to_cart", "value": "69890"},
                {"action_type": "like", "value": "6"},
                {"action_type": "onsite_web_add_to_cart", "value": "69890"},
                {"action_type": "onsite_web_view_content", "value": "20571"},
                {"action_type": "video_view", "value": "939594"},
                {"action_type": "omni_view_content", "value": "20571"},
                {
                    "action_type": "offsite_conversion.fb_pixel_view_content",
                    "value": "20524",
                },
                {"action_type": "post_reaction", "value": "7220"},
                {
                    "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                    "value": "69890",
                },
                {
                    "action_type": "offsite_conversion.fb_pixel_purchase",
                    "value": "4080",
                },
                {"action_type": "omni_add_to_wishlist", "value": "1"},
                {"action_type": "link_click", "value": "59552"},
                {"action_type": "omni_purchase", "value": "4080"},
            ],
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        }
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "action_type": [
                "onsite_conversion.post_save",
                "onsite_conversion.view_content",
                "onsite_conversion.add_to_wishlist",
                "post",
                "onsite_web_app_view_content",
                "landing_page_view",
                "omni_add_to_cart",
                "onsite_web_app_add_to_cart",
                "comment",
                "onsite_web_app_purchase",
                "page_engagement",
                "purchase",
                "post_engagement",
                "onsite_web_purchase",
                "view_content",
                "onsite_app_view_content",
                "add_to_cart",
                "like",
                "onsite_web_add_to_cart",
                "onsite_web_view_content",
                "video_view",
                "omni_view_content",
                "offsite_conversion.fb_pixel_view_content",
                "post_reaction",
                "offsite_conversion.fb_pixel_add_to_cart",
                "offsite_conversion.fb_pixel_purchase",
                "omni_add_to_wishlist",
                "link_click",
                "omni_purchase",
            ],
            "actions": [
                "807",
                "47",
                "1",
                "395",
                "20571",
                "42096",
                "69890",
                "69890",
                "1054",
                "4080",
                "1008628",
                "4080",
                "1008622",
                "4080",
                "20524",
                "47",
                "69890",
                "6",
                "69890",
                "20571",
                "939594",
                "20571",
                "20524",
                "7220",
                "69890",
                "4080",
                "1",
                "59552",
                "4080",
            ],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_complex_action() -> None:
    sql_parts = QueryArgs(
        metrics=["actions", "impressions"],
        group_by_columns=["action_type", "gender"],
        date_ranges="(2023-02-06,2024-02-06)",
    )
    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "actions": [
                {"action_type": "onsite_conversion.post_save", "value": "317"},
                {"action_type": "onsite_conversion.view_content", "value": "12"},
                {"action_type": "post", "value": "188"},
                {"action_type": "onsite_web_app_view_content", "value": "7618"},
                {"action_type": "landing_page_view", "value": "13477"},
                {"action_type": "omni_add_to_cart", "value": "25603"},
                {"action_type": "onsite_web_app_add_to_cart", "value": "25603"},
                {"action_type": "comment", "value": "313"},
                {"action_type": "onsite_web_app_purchase", "value": "1612"},
                {"action_type": "page_engagement", "value": "255098"},
                {"action_type": "purchase", "value": "1612"},
                {"action_type": "post_engagement", "value": "255097"},
                {"action_type": "onsite_web_purchase", "value": "1612"},
                {"action_type": "view_content", "value": "7606"},
                {"action_type": "onsite_app_view_content", "value": "12"},
                {"action_type": "add_to_cart", "value": "25603"},
                {"action_type": "like", "value": "1"},
                {"action_type": "onsite_web_add_to_cart", "value": "25603"},
                {"action_type": "onsite_web_view_content", "value": "7618"},
                {"action_type": "video_view", "value": "234219"},
                {"action_type": "omni_view_content", "value": "7618"},
                {
                    "action_type": "offsite_conversion.fb_pixel_view_content",
                    "value": "7606",
                },
                {"action_type": "post_reaction", "value": "1884"},
                {
                    "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                    "value": "25603",
                },
                {
                    "action_type": "offsite_conversion.fb_pixel_purchase",
                    "value": "1612",
                },
                {"action_type": "link_click", "value": "18176"},
                {"action_type": "omni_purchase", "value": "1612"},
            ],
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "female",
            "impressions": "1861808",
        },
        {
            "actions": [
                {"action_type": "onsite_conversion.post_save", "value": "483"},
                {"action_type": "onsite_conversion.view_content", "value": "35"},
                {"action_type": "onsite_conversion.add_to_wishlist", "value": "1"},
                {"action_type": "post", "value": "205"},
                {"action_type": "onsite_web_app_view_content", "value": "12730"},
                {"action_type": "landing_page_view", "value": "28075"},
                {"action_type": "omni_add_to_cart", "value": "43600"},
                {"action_type": "onsite_web_app_add_to_cart", "value": "43600"},
                {"action_type": "comment", "value": "722"},
                {"action_type": "onsite_web_app_purchase", "value": "2419"},
                {"action_type": "page_engagement", "value": "737278"},
                {"action_type": "purchase", "value": "2419"},
                {"action_type": "post_engagement", "value": "737274"},
                {"action_type": "onsite_web_purchase", "value": "2419"},
                {"action_type": "view_content", "value": "12695"},
                {"action_type": "onsite_app_view_content", "value": "35"},
                {"action_type": "add_to_cart", "value": "43600"},
                {"action_type": "like", "value": "4"},
                {"action_type": "onsite_web_add_to_cart", "value": "43600"},
                {"action_type": "onsite_web_view_content", "value": "12730"},
                {"action_type": "video_view", "value": "690163"},
                {"action_type": "omni_view_content", "value": "12730"},
                {
                    "action_type": "offsite_conversion.fb_pixel_view_content",
                    "value": "12695",
                },
                {"action_type": "post_reaction", "value": "5246"},
                {
                    "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                    "value": "43600",
                },
                {
                    "action_type": "offsite_conversion.fb_pixel_purchase",
                    "value": "2419",
                },
                {"action_type": "omni_add_to_wishlist", "value": "1"},
                {"action_type": "link_click", "value": "40455"},
                {"action_type": "omni_purchase", "value": "2419"},
            ],
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "male",
            "impressions": "4359639",
        },
        {
            "actions": [
                {"action_type": "onsite_conversion.post_save", "value": "7"},
                {"action_type": "post", "value": "2"},
                {"action_type": "onsite_web_app_view_content", "value": "223"},
                {"action_type": "landing_page_view", "value": "544"},
                {"action_type": "omni_add_to_cart", "value": "687"},
                {"action_type": "onsite_web_app_add_to_cart", "value": "687"},
                {"action_type": "comment", "value": "19"},
                {"action_type": "onsite_web_app_purchase", "value": "49"},
                {"action_type": "page_engagement", "value": "16252"},
                {"action_type": "purchase", "value": "49"},
                {"action_type": "post_engagement", "value": "16251"},
                {"action_type": "onsite_web_purchase", "value": "49"},
                {"action_type": "view_content", "value": "223"},
                {"action_type": "add_to_cart", "value": "687"},
                {"action_type": "like", "value": "1"},
                {"action_type": "onsite_web_add_to_cart", "value": "687"},
                {"action_type": "onsite_web_view_content", "value": "223"},
                {"action_type": "video_view", "value": "15212"},
                {"action_type": "omni_view_content", "value": "223"},
                {
                    "action_type": "offsite_conversion.fb_pixel_view_content",
                    "value": "223",
                },
                {"action_type": "post_reaction", "value": "90"},
                {
                    "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                    "value": "687",
                },
                {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "49"},
                {"action_type": "link_click", "value": "921"},
                {"action_type": "omni_purchase", "value": "49"},
            ],
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "unknown",
            "impressions": "91839",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "gender": [
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "female",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "male",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
            ],
            "impressions": [
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "1861808",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "4359639",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
                "91839",
            ],
            "action_type": [
                "onsite_conversion.post_save",
                "onsite_conversion.view_content",
                "post",
                "onsite_web_app_view_content",
                "landing_page_view",
                "omni_add_to_cart",
                "onsite_web_app_add_to_cart",
                "comment",
                "onsite_web_app_purchase",
                "page_engagement",
                "purchase",
                "post_engagement",
                "onsite_web_purchase",
                "view_content",
                "onsite_app_view_content",
                "add_to_cart",
                "like",
                "onsite_web_add_to_cart",
                "onsite_web_view_content",
                "video_view",
                "omni_view_content",
                "offsite_conversion.fb_pixel_view_content",
                "post_reaction",
                "offsite_conversion.fb_pixel_add_to_cart",
                "offsite_conversion.fb_pixel_purchase",
                "link_click",
                "omni_purchase",
                "onsite_conversion.post_save",
                "onsite_conversion.view_content",
                "onsite_conversion.add_to_wishlist",
                "post",
                "onsite_web_app_view_content",
                "landing_page_view",
                "omni_add_to_cart",
                "onsite_web_app_add_to_cart",
                "comment",
                "onsite_web_app_purchase",
                "page_engagement",
                "purchase",
                "post_engagement",
                "onsite_web_purchase",
                "view_content",
                "onsite_app_view_content",
                "add_to_cart",
                "like",
                "onsite_web_add_to_cart",
                "onsite_web_view_content",
                "video_view",
                "omni_view_content",
                "offsite_conversion.fb_pixel_view_content",
                "post_reaction",
                "offsite_conversion.fb_pixel_add_to_cart",
                "offsite_conversion.fb_pixel_purchase",
                "omni_add_to_wishlist",
                "link_click",
                "omni_purchase",
                "onsite_conversion.post_save",
                "post",
                "onsite_web_app_view_content",
                "landing_page_view",
                "omni_add_to_cart",
                "onsite_web_app_add_to_cart",
                "comment",
                "onsite_web_app_purchase",
                "page_engagement",
                "purchase",
                "post_engagement",
                "onsite_web_purchase",
                "view_content",
                "add_to_cart",
                "like",
                "onsite_web_add_to_cart",
                "onsite_web_view_content",
                "video_view",
                "omni_view_content",
                "offsite_conversion.fb_pixel_view_content",
                "post_reaction",
                "offsite_conversion.fb_pixel_add_to_cart",
                "offsite_conversion.fb_pixel_purchase",
                "link_click",
                "omni_purchase",
            ],
            "actions": [
                "317",
                "12",
                "188",
                "7618",
                "13477",
                "25603",
                "25603",
                "313",
                "1612",
                "255098",
                "1612",
                "255097",
                "1612",
                "7606",
                "12",
                "25603",
                "1",
                "25603",
                "7618",
                "234219",
                "7618",
                "7606",
                "1884",
                "25603",
                "1612",
                "18176",
                "1612",
                "483",
                "35",
                "1",
                "205",
                "12730",
                "28075",
                "43600",
                "43600",
                "722",
                "2419",
                "737278",
                "2419",
                "737274",
                "2419",
                "12695",
                "35",
                "43600",
                "4",
                "43600",
                "12730",
                "690163",
                "12730",
                "12695",
                "5246",
                "43600",
                "2419",
                "1",
                "40455",
                "2419",
                "7",
                "2",
                "223",
                "544",
                "687",
                "687",
                "19",
                "49",
                "16252",
                "49",
                "16251",
                "49",
                "223",
                "687",
                "1",
                "687",
                "223",
                "15212",
                "223",
                "223",
                "90",
                "687",
                "49",
                "921",
                "49",
            ],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_respons_double_action() -> None:
    sql_parts = QueryArgs(
        metrics=["actions", "action_values"],
        group_by_columns=["action_type"],
        date_ranges="(2023-02-06,2024-02-06)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "action_values": [
                {"action_type": "onsite_web_app_purchase", "value": "269114.59"},
                {"action_type": "omni_purchase", "value": "269114.59"},
                {
                    "action_type": "offsite_conversion.fb_pixel_purchase",
                    "value": "269114.59",
                },
                {"action_type": "purchase", "value": "269114.59"},
                {"action_type": "onsite_web_purchase", "value": "269114.59"},
            ],
            "actions": [
                {"action_type": "onsite_conversion.post_save", "value": "807"},
                {"action_type": "onsite_conversion.view_content", "value": "47"},
                {"action_type": "onsite_conversion.add_to_wishlist", "value": "1"},
                {"action_type": "post", "value": "395"},
                {"action_type": "onsite_web_app_view_content", "value": "20571"},
                {"action_type": "landing_page_view", "value": "42096"},
                {"action_type": "omni_add_to_cart", "value": "69890"},
                {"action_type": "onsite_web_app_add_to_cart", "value": "69890"},
                {"action_type": "comment", "value": "1054"},
                {"action_type": "onsite_web_app_purchase", "value": "4080"},
                {"action_type": "page_engagement", "value": "1008628"},
                {"action_type": "purchase", "value": "4080"},
                {"action_type": "post_engagement", "value": "1008622"},
                {"action_type": "onsite_web_purchase", "value": "4080"},
                {"action_type": "view_content", "value": "20524"},
                {"action_type": "onsite_app_view_content", "value": "47"},
                {"action_type": "add_to_cart", "value": "69890"},
                {"action_type": "like", "value": "6"},
                {"action_type": "onsite_web_add_to_cart", "value": "69890"},
                {"action_type": "onsite_web_view_content", "value": "20571"},
                {"action_type": "video_view", "value": "939594"},
                {"action_type": "omni_view_content", "value": "20571"},
                {
                    "action_type": "offsite_conversion.fb_pixel_view_content",
                    "value": "20524",
                },
                {"action_type": "post_reaction", "value": "7220"},
                {
                    "action_type": "offsite_conversion.fb_pixel_add_to_cart",
                    "value": "69890",
                },
                {
                    "action_type": "offsite_conversion.fb_pixel_purchase",
                    "value": "4080",
                },
                {"action_type": "omni_add_to_wishlist", "value": "1"},
                {"action_type": "link_click", "value": "59552"},
                {"action_type": "omni_purchase", "value": "4080"},
            ],
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
        }
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "action_type": [
                "onsite_conversion.post_save",
                "onsite_conversion.view_content",
                "onsite_conversion.add_to_wishlist",
                "post",
                "onsite_web_app_view_content",
                "landing_page_view",
                "omni_add_to_cart",
                "onsite_web_app_add_to_cart",
                "comment",
                "onsite_web_app_purchase",
                "page_engagement",
                "purchase",
                "post_engagement",
                "onsite_web_purchase",
                "view_content",
                "onsite_app_view_content",
                "add_to_cart",
                "like",
                "onsite_web_add_to_cart",
                "onsite_web_view_content",
                "video_view",
                "omni_view_content",
                "offsite_conversion.fb_pixel_view_content",
                "post_reaction",
                "offsite_conversion.fb_pixel_add_to_cart",
                "offsite_conversion.fb_pixel_purchase",
                "omni_add_to_wishlist",
                "link_click",
                "omni_purchase",
            ],
            "action_values": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "269114.59",
                np.nan,
                "269114.59",
                np.nan,
                "269114.59",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "269114.59",
                np.nan,
                np.nan,
                "269114.59",
            ],
            "actions": [
                "807",
                "47",
                "1",
                "395",
                "20571",
                "42096",
                "69890",
                "69890",
                "1054",
                "4080",
                "1008628",
                "4080",
                "1008622",
                "4080",
                "20524",
                "47",
                "69890",
                "6",
                "69890",
                "20571",
                "939594",
                "20571",
                "20524",
                "7220",
                "69890",
                "4080",
                "1",
                "59552",
                "4080",
            ],
        }
    )

    # Sort the result and expected DataFrames by the "action_type" column
    result_df = result[0].sort_values(by="action_type").reset_index(drop=True)
    expected_result = expected_result.sort_values(by="action_type").reset_index(
        drop=True
    )

    result_df["action_values"] = pd.to_numeric(
        result_df["action_values"], errors="coerce"
    )
    expected_result["action_values"] = pd.to_numeric(
        expected_result["action_values"], errors="coerce"
    )

    # Check if the sorted result DataFrame matches the sorted expected DataFrame
    try:
        pd.testing.assert_frame_equal(result_df, expected_result)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_multiple_date_ranges_1() -> None:
    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["gender"],
        date_ranges="(2023-11-01,2023-11-30), (2023-12-01,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "date_start": "2023-11-01",
            "date_stop": "2023-11-30",
            "gender": "female",
            "impressions": "701398",
        },
        {
            "date_start": "2023-11-01",
            "date_stop": "2023-11-30",
            "gender": "male",
            "impressions": "1258016",
        },
        {
            "date_start": "2023-11-01",
            "date_stop": "2023-11-30",
            "gender": "unknown",
            "impressions": "30578",
        },
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "female",
            "impressions": "1861808",
        },
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "male",
            "impressions": "4359639",
        },
        {
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "gender": "unknown",
            "impressions": "91839",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = [
        pd.DataFrame(
            {
                "gender": ["female", "male", "unknown"],
                "impressions": ["1861808", "4359639", "91839"],
            }
        ),
        pd.DataFrame(
            {
                "gender": ["female", "male", "unknown"],
                "impressions": ["701398", "1258016", "30578"],
            }
        ),
    ]

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result[0], check_like=True)
        pd.testing.assert_frame_equal(result[1], expected_result[1], check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_multiple_date_ranges_2() -> None:
    sql_parts = QueryArgs(
        metrics=["reach", "frequency"],
        group_by_columns=["yearMonth"],
        date_ranges="(2024-01-01,2024-01-31), (2024-02-01,2024-02-28)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "date_start": "2024-01-01",
            "date_stop": "2024-01-31",
            "frequency": "3.171696",
            "reach": "2263706",
        },
        {
            "date_start": "2024-02-01",
            "date_stop": "2024-02-28",
            "frequency": "3.415211",
            "reach": "1435284",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = [
        pd.DataFrame(
            {
                "frequency": ["3.42"],
                "reach": ["1435284"],
                "yearMonth": ["2024-02"],
            }
        ),
        pd.DataFrame(
            {
                "frequency": ["3.17"],
                "reach": ["2263706"],
                "yearMonth": ["2024-01"],
            }
        ),
    ]

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(
            result[0].reset_index(drop=True), expected_result[0], check_like=True
        )
        pd.testing.assert_frame_equal(
            result[1].reset_index(drop=True), expected_result[1], check_like=True
        )
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_response_missing_date_range() -> None:
    sql_parts = QueryArgs(
        metrics=["impressions"],
        group_by_columns=["country"],
        date_ranges="(2023-10-01,2023-10-31), (2023-12-01,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "country": "CA",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "impressions": "1017386",
        },
        {
            "country": "GB",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "impressions": "2375660",
        },
        {
            "country": "US",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "impressions": "2920240",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = [
        pd.DataFrame(
            {
                "country": ["CA", "GB", "US"],
                "impressions": ["1017386", "2375660", "2920240"],
            }
        ),
        pd.DataFrame(
            {
                "country": ["CA", "GB", "US"],
                "impressions": [np.nan, np.nan, np.nan],
            }
        ).astype({"impressions": "object"}),
    ]

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result[0], check_like=True)
        pd.testing.assert_frame_equal(result[1], expected_result[1], check_like=True)
    except AssertionError as e:
        raise


@pytest.mark.asyncio
async def test_parse_report_cap_float() -> None:
    sql_parts = QueryArgs(
        metrics=["ctr"],
        group_by_columns=["country"],
        date_ranges="(2023-10-01,2023-10-31), (2023-12-01,2023-12-31)",
    )

    # Mock AdReportRun with a dummy ID
    mock_ad_report_run = MagicMock(spec=AdReportRun)
    mock_ad_report_run.get_id_assured.return_value = "dummy_id"

    # Create an AdsInsights object and set its data
    data = [
        {
            "country": "CA",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "ctr": "2.63281",
        },
        {
            "country": "GB",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "ctr": "1.8313731",
        },
        {
            "country": "US",
            "date_start": "2023-12-01",
            "date_stop": "2023-12-31",
            "ctr": "5.788121",
        },
    ]
    report_response = []
    for ads_insight_data in data:
        ads_insight = AdsInsights()
        ads_insight.set_data(ads_insight_data)
        report_response.append(ads_insight)

    result = await FB_PARSER.parse_report_response_to_dataframe(
        report_response=report_response,
        query_args=sql_parts,
        logger=LOGGER,
    )

    expected_result = pd.DataFrame(
        {
            "country": ["CA", "GB", "US"],
            "ctr": ["2.63", "1.83", "5.79"],
        }
    )

    # Check if the result dataframe matches the expected dataframe
    try:
        pd.testing.assert_frame_equal(result[0], expected_result, check_like=True)
    except AssertionError as e:
        raise e
