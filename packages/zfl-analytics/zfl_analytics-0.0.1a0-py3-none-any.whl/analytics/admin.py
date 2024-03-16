from django.contrib import admin  # type: ignore
from django.shortcuts import redirect  # type: ignore

from .forms import AnalyticsAppSettingsForm
from .models import AnalyticsAppSettings, DimensionDate, GoogleAnalytics4Config


class AnalyticsAppSettingsAdmin(admin.ModelAdmin):
    form = AnalyticsAppSettingsForm
    fieldsets = (
        ("ベースHTMLファイル設定", {"fields": ("base_html_file",)}),
        ("ページの編集", {"fields": ("nav_title", "heading_ja", "heading_us")}),
        (
            "レイアウトの調整",
            {
                "fields": (
                    "container",
                    ("col_left", "col_center", "col_right"),
                )
            },
        ),
    )

    def response_post_save_change(self, request, obj):  # noqa: ARG002
        return redirect("analytics:index")


class GoogleAnalytics4ConfigAdmin(admin.ModelAdmin):
    def response_post_save_change(self, request, obj):  # noqa: ARG002
        return redirect("analytics:index")


admin.site.register(AnalyticsAppSettings, AnalyticsAppSettingsAdmin)
admin.site.register(GoogleAnalytics4Config, GoogleAnalytics4ConfigAdmin)
admin.site.register(DimensionDate)

# Register your models here.
