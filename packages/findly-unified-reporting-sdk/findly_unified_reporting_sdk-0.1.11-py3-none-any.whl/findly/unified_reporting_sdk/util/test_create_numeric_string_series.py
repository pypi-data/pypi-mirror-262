import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from findly.unified_reporting_sdk.util.create_numeric_string_series import create_numeric_string_series


def test_create_numeric_string_series() -> None:
    # Test case 1: All values are integers
    col1 = pd.Series([1, 2, 3, 4, 5])
    expected_result1 = pd.Series(['1', '2', '3', '4', '5'])
    result1 = create_numeric_string_series(col1)
    assert_series_equal(result1, expected_result1)

    # Test case 2: Values are floats
    col2 = pd.Series([1.234, 2.345, 3.456, 4.567, 5.678])
    expected_result2 = pd.Series(['1.23', '2.35', '3.46', '4.57', '5.68'])
    result2 = create_numeric_string_series(col2)
    assert_series_equal(result2, expected_result2)

    # Test case 3: Values are a mix of integers and floats
    col3 = pd.Series([1, 2.345, 3, 4.567, 5])
    expected_result3 = pd.Series(['1.0', '2.35', '3.0', '4.57', '5.0'])
    result3 = create_numeric_string_series(col3)
    assert_series_equal(result3, expected_result3)

    # Test case 4: Empty series
    col4 = pd.Series([])
    expected_result4 = pd.Series([])
    result4 = create_numeric_string_series(col4)
    assert_series_equal(result4, expected_result4)

    # Test case 5: Series with non-numeric values
    col5 = pd.Series(['a', 'b', 'c'])
    expected_result5 = pd.Series(['a', 'b', 'c'])
    result5 = create_numeric_string_series(col5)
    assert_series_equal(result5, expected_result5)

    # Test case 6: Exception handling
    col6 = pd.Series([1, 2, 3])
    with pytest.raises(Exception):
        result6 = create_numeric_string_series(col6)
        assert_series_equal(result6, col6)
