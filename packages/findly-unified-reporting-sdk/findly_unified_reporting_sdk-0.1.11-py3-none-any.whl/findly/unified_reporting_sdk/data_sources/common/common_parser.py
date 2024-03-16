import re
import pandas as pd
from datetime import datetime
from typing import List, Optional, Callable, Tuple, Any
from findly.unified_reporting_sdk.protos.findly_semantic_layer_pb2 import QueryArgs
from findly.unified_reporting_sdk.data_sources.common.date_range_helper import (
    get_time_today,
    get_time_1_years_ago,
    parse_datetime_tuple,
)

NONE_VALUE = "none"
RESERVED_TOTAL = "RESERVED_TOTAL"


class CommonParser:
    def __init__(self) -> None:
        pass

    @classmethod
    def default(
        cls,
    ) -> "CommonParser":
        return cls()

    def parse_string_list(
        self,
        string_list: Optional[str],
    ) -> Optional[List[str]]:
        if string_list is None:
            return None

        string_list = string_list.strip().strip("]").strip("[").strip("'")

        if string_list == "":
            return []

        if string_list.lower() == NONE_VALUE:
            return None

        column_names_selected = re.split(r'[,\s\r\n]+', string_list.strip(' []'))

        # Remove the quotes and spaces from the column names.
        cleaned_column_names: List[str] = [
            column.strip().strip("'").strip('"') for column in column_names_selected
        ]

        # Remove empty strings from the list, if any. and make the list unique.
        cleaned_column_names = [
            column for column in cleaned_column_names if column != ""
        ]

        if len(cleaned_column_names) == 0 or cleaned_column_names == [""]:
            return []

        if cleaned_column_names == [NONE_VALUE]:
            return None

        return cleaned_column_names

    async def get_date_ranges(
        self,
        date_where_clause_str: Optional[str],
        format_function: Callable[[str, str], Any] = lambda start, end: {
            "since": start,
            "until": end,
        },
    ) -> List[Any]:
        default_start_date = get_time_1_years_ago()
        default_end_date = get_time_today()

        if (
            date_where_clause_str is None
            or date_where_clause_str.strip() == ""
            or date_where_clause_str.strip().lower() == NONE_VALUE
        ):
            return [format_function(default_start_date, default_end_date)]

        # You have a string in the format: "(start_date, end_date), (start_date, end_date), ...".
        # You want to parse it into a list of DateRange objects.
        # You can use the parse_datetime_tuple function to parse each tuple.

        # First remove all the extra spaces of the date_where_clause_str.
        date_where_clause_str = date_where_clause_str.replace(" ", "")
        date_where_clause_list = date_where_clause_str.split("),")

        date_ranges_objects = []

        for date_where_clause in date_where_clause_list:
            try:
                date_where_clause_tuple: Optional[Tuple] = parse_datetime_tuple(
                    date_where_clause
                )

                if date_where_clause_tuple is None:
                    return [format_function(default_start_date, default_end_date)]

                start_date, end_date = date_where_clause_tuple
                if (
                    start_date is not None
                    and start_date.strip() != ""
                    and start_date.strip().lower() != NONE_VALUE
                ):
                    start_date = start_date.strip().replace("'", "")
                else:
                    start_date = default_start_date
                if (
                    end_date is not None
                    and end_date.strip() != ""
                    and end_date.strip().lower() != NONE_VALUE
                ):
                    end_date = end_date.strip().replace("'", "")
                else:
                    end_date = default_end_date

                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

                date_ranges_objects.append(
                    (
                        start_date_obj,
                        end_date_obj,
                    )
                )
            except Exception:
                return [format_function(default_start_date, default_end_date)]

        # Sort the date_ranges list in descending order based on end_date
        # If the end_date is the same, sort in descending order based on start_date
        date_ranges_objects.sort(key=lambda x: (x[1], x[0]), reverse=True)

        # Convert back to string format
        date_ranges = []
        for range_obj in date_ranges_objects:
            str_start_date = range_obj[0].strftime("%Y-%m-%d")
            str_end_date = range_obj[1].strftime("%Y-%m-%d")
            formated_date_range = format_function(str_start_date, str_end_date)
            date_ranges.append(formated_date_range)

        return date_ranges

    async def parse_query_args_to_sql(
        self, query: QueryArgs
    ) -> str:
        """
        Parses the QueryArgs object into a SQL query.

        Args:
            query (QueryArgs): The query args object.

        Returns:
            str: The SQL query generated from the QueryArgs object.
        """
        query_parts = []

        select_parts = []
        # Metrics and Metrics Expression
        if query.metrics:
            select_parts.append(", ".join(query.metrics))
        elif query.metrics_expression:
            select_parts.append(", ".join(query.metrics_expression))
        if query.group_by_columns:
            select_parts.append(", ".join(query.group_by_columns))
        if len(select_parts) > 0:
            select_str = "SELECT " + ", ".join(select_parts)
            query_parts.append(select_str)

        # Where clause
        conditions = []
        if query.where_clause:
            where_clause_modified = re.sub(
                r"\bwhere\b", "", query.where_clause, flags=re.IGNORECASE
            ).strip()
            conditions.append(f"WHERE {where_clause_modified}")

        # Date Where clause
        if query.date_ranges:
            sql_date_range = await self.get_date_ranges(
                date_where_clause_str=query.date_ranges
            )
            for date_range in sql_date_range:
                start_date = date_range["since"]
                end_date = date_range["until"]
                # Check if start and end dates are the same
                if start_date == end_date:
                    # Use equality condition when dates are the same
                    conditions.append(f"date = '{start_date}'")
                else:
                    # Use BETWEEN when dates are different
                    conditions.append(f"date BETWEEN '{start_date}' AND '{end_date}'")

        if conditions:
            query_parts.append(f"{' AND '.join(conditions)}")

        # Group By
        if query.group_by_columns:
            group_by_str = ", ".join(query.group_by_columns)
            query_parts.append(f"GROUP BY {group_by_str}")

        # Having
        if query.having_clause:
            having_clause_modified = re.sub(
                r"\bhaving\b", "", query.having_clause, flags=re.IGNORECASE
            ).strip()
            query_parts.append(f"HAVING {having_clause_modified }")

        # Order By
        if query.order_by:
            query_parts.append(f"ORDER BY {query.order_by}")

        # Limit
        if query.limit:
            query_parts.append(f"LIMIT {query.limit}")

        return "\n".join(query_parts)

    def equalize_dataframe_rows(
        self, dataframes: List[pd.DataFrame], dimensions: List[str]
    ) -> List[pd.DataFrame]:
        if len(dataframes) <= 1 or not dimensions:
            return dataframes

        # Check if all dimensions exist in all dataframes
        if not all(all(dim in df.columns for dim in dimensions) for df in dataframes):
            return dataframes

        # Combine all dataframes into one to get all unique combinations of dimension values
        combined_df = pd.concat(dataframes)
        unique_combinations = combined_df[dimensions].drop_duplicates()

        # Create a list to store the equalized dataframes
        equalized_dataframes = []

        # For each dataframe, merge it with the DataFrame of unique combinations
        for i, df in enumerate(dataframes):
            equalized_df = pd.merge(unique_combinations, df, how="left", on=dimensions)
            equalized_df["origin"] = i
            equalized_dataframes.append(equalized_df)

        # Sort the combined dataframe by the 'origin' column to preserve the original order
        combined_df = pd.concat(equalized_dataframes)
        combined_df.sort_values(by="origin", inplace=True)

        # Split the combined dataframe back into individual dataframes
        equalized_dataframes = [
            df.drop(columns="origin").reset_index(drop=True)
            for _, df in combined_df.groupby("origin")
        ]

        # Ensure that rows with RESERVED_TOTAL are always the last row in each dataframe
        for df in equalized_dataframes:
            df["sort"] = df.index
            for dimension in dimensions:
                df["sort"] = df["sort"].where(
                    df[dimension] != RESERVED_TOTAL, df["sort"] + len(df)
                )
            df.sort_values(by="sort", inplace=True)
            df.drop("sort", axis=1, inplace=True)
            df.reset_index(drop=True, inplace=True)

        return equalized_dataframes
