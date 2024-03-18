from django.contrib.auth.models import User  # type: ignore
from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

from analytics.models import AnalyticsAppSettings, GoogleAnalytics4Config


class AnalyticsAppSettingsAdminTests(TestCase):
    """管理画面でのアナリティクスアプリ設定変更画面"""

    def test_analytics_set_post_redirect(self):
        """アナリティクスアプリの設定が保存され、リダイレクト先へ遷移するテスト"""
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
                "col_right": 2,
            },
        )
        redirect_url = reverse("analytics:index")
        self.assertRedirects(response, redirect_url)


class GoogleAnalytics4ConfigAdminTests(TestCase):
    """管理画面でのGA4構成変更画面"""

    def test_ga4_config_post_redirect(self):
        """GA4の構成が保存され、リダイレクト先へ遷移するテスト"""
        admin_user = User.objects.create(
            username="myuser", is_superuser=True, is_staff=True
        )
        self.client.force_login(admin_user)
        ga4_config = GoogleAnalytics4Config.objects.create(
            author=admin_user,
            property_id=1111,
            days_ago=7,
        )
        url = reverse(
            "admin:analytics_googleanalytics4config_change", args=(ga4_config.id,)
        )
        response = self.client.post(
            path=url,
            data={
                "author": admin_user.id,
                "property_id": 1111,
                "days_ago": 14,
            },
        )
        redirect_url = reverse("analytics:index")
        self.assertRedirects(response, redirect_url)
