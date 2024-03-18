from django.contrib.auth.models import User  # type: ignore
from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

from analytics.models import AnalyticsAppSettings


class AnalyticsAppSettingsFormTests(TestCase):
    """管理画面でのアナリティクスアプリ設定変更画面"""

    def test_analytics_set_clean(self):
        """アナリティクスアプリの設定が保存され、バリデーションエラーを出力するテスト"""

        admin_user = User.objects.create(
            username="myuser", is_superuser=True, is_staff=True
        )
        self.client.force_login(admin_user)
        analytics_set = AnalyticsAppSettings.objects.create()
        url = reverse(
            "admin:analytics_analyticsappsettings_change", args=(analytics_set.id,)
        )
        response = self.client.post(
            path=url,
            data={
                "nav_title": "アナリティクス",
                "heading_ja": "ようこそアナリティクスページへ",
                "heading_us": "Welcome to analytics page",
                "base_html_file": "base.html",
                "container": "",
                "col_left": 2,
                "col_center": 8,
                "col_right": 3,
            },
        )
        error_text = "「レイアウト調整」のカラム総数が13です。\n12に合わせる必要があります。"
        self.assertContains(response, error_text)
