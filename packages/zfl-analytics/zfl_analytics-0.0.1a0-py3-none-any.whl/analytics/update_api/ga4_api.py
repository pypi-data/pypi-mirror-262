from google.analytics.data_v1beta import BetaAnalyticsDataClient  # type: ignore
from google.analytics.data_v1beta.types import (  # type: ignore
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)


def run_report(property_id, start_date, end_date):
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="NewUsers"),
            Metric(name="screenPageViews"),
            Metric(name="sessions"),
            Metric(name="totalAdRevenue"),
            Metric(name="publisherAdImpressions"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)

    res_dict: dict = {}

    # ディメンション値のキーバリューを作成
    # {'dimension_header':['dimension_value', 'dimension_value', ...]}
    for i, row in enumerate(response.dimension_headers):
        # print(row.name)
        res_dict[row.name] = [row.dimension_values[i].value for row in response.rows]

    # メトリック値のキーバリューを作成
    # {'metric_header':['metric_value', 'metric_value', ...]}
    for i, row in enumerate(response.metric_headers):
        # print(i, row.name)
        res_dict[row.name] = [row.metric_values[i].value for row in response.rows]

    return res_dict
