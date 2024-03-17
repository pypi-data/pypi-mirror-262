from django.contrib.auth.models import User  # type: ignore
from django.test import TestCase  # type: ignore
from django.utils import timezone  # type: ignore

from analytics.models import AnalyticsAppSettings, DimensionDate, GoogleAnalytics4Config
from analytics.safety.function import encryption


class AnalyticsAppSettingsTests(TestCase):
    """AnalyticsAppSettingsモデル"""

    def test_base_index_html_save(self):
        """base_index_htmlフィールドの値が変更され保存された際のテスト"""

        import os
        import re

        from django.conf import settings  # type: ignore

        basehtml_file = "analytics/templates/analytics/base_index.html"
        file_dir = os.path.join(settings.BASE_DIR, basehtml_file)
        with open(file_dir) as f:
            html_text = f.read()
        base_html_file = "analytics/base.html"
        existing_name = re.search("^" + base_html_file, html_text)
        if not existing_name:
            AnalyticsAppSettings.objects.create(base_html_file=base_html_file)
        # アサートに使用する値
        aas = AnalyticsAppSettings.objects.all().first()
        with open(file_dir) as f:
            html_text = f.read()
        comp = re.compile(r"extends '\w+.html|extends '\w+/\w+.html")
        re_obj = comp.search(html_text)
        if re_obj:
            html_text = re_obj.group().replace("extends '", "")
        # Assert
        self.assertEqual(aas.base_html_file, html_text)
        # extends 'analytics/base.html'になってしまったのを戻す
        aas.base_html_file = "base.html"
        aas.save()


class DimensionDateTests(TestCase):
    """DimensionDateモデル"""

    def test_str_method_returns_dates(self):
        """
        strメソッドではdatesの値が返される。
        """

        date = timezone.now().date()
        dimensiondate = DimensionDate(
            dates=date,
            users=1,
            new_users=1,
            page_views=1,
            sessions=1,
            ad_revenue=1,
            ad_impressions=1,
        )
        self.assertEqual(dimensiondate.__str__(), str(date))


class GoogleAnalytics4ConfigTests(TestCase):
    """GoogleAnalytics4Configモデル"""

    def test_save_property_id_encrypt(self):
        """プロパティIDが保存される前に暗号化されるかテスト"""

        encrypt = encryption("0123")
        admin_user = User.objects.create(
            username="myuser", is_superuser=True, is_staff=True
        )
        self.client.force_login(admin_user)
        ga4_config = GoogleAnalytics4Config.objects.create(
            author=admin_user,
            property_id=encrypt,
            days_ago=7,
        )
        # Assert
        self.assertEqual(ga4_config.property_id, encrypt)
