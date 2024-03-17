from django.core.management.base import BaseCommand  # type: ignore

from analytics.models import AnalyticsAppSettings


class Command(BaseCommand):
    def handle(self, **options):  # noqa: ARG002
        try:
            AnalyticsAppSettings.objects.create(
                nav_title="アナリティクス",
                heading_ja="ようこそアナリティクスページへ",
                heading_us="Welcome to analytics page",
            )
            success_text = "アナリティクスアプリの初期設定完了"
            self.stdout.write(self.style.SUCCESS(success_text))
        except Exception as inst:
            Exception(inst)
            error_text = "先に「python3 manage.py migrate」を実行してください"
            self.stdout.write(self.style.ERROR(error_text))
