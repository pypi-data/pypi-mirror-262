import pandas as pd
from django.utils import timezone  # type: ignore

from analytics.models import DimensionDate
from analytics.safety.function import decryption

from .ga4_api import run_report


def update_analyticsdata(ga4_config):
    property_id = decryption(ga4_config.property_id)
    days_ago = ga4_config.days_ago
    # 本日から数日前までのアナリティクスデータを更新する処理
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=days_ago)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    res_dict = run_report(property_id, start_date, end_date)
    df = pd.DataFrame(res_dict)
    df.columns = [
        "Date",
        "Users",
        "NewUsers",
        "PageView",
        "Sessions",
        "Revenue",
        "AdImpressions",
    ]
    df = df.sort_values("Date").reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Revenue"] = round(df["Revenue"].astype(float)).astype(int)

    for index, row in df.iterrows():  # noqa: B007
        DimensionDate.objects.update_or_create(
            dates=row.Date,
            defaults={
                "users": row.Users,
                "new_users": row.NewUsers,
                "page_views": row.PageView,
                "sessions": row.Sessions,
                "ad_revenue": row.Revenue,
                "ad_impressions": row.AdImpressions,
            },
        )
