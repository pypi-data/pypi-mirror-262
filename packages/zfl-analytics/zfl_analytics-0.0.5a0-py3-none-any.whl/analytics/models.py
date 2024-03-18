from django.contrib.auth import get_user_model  # type: ignore
from django.core.validators import MaxValueValidator, MinValueValidator  # type: ignore
from django.db import models  # type: ignore

from analytics.safety.function import decryption, encryption


class AnalyticsAppSettings(models.Model):
    CONTAINER_CHOICES = (
        ("", "無効"),
        ("container", "container"),
        ("container-sm", "container-sm"),
        ("container-fluid", "container-fluid"),
    )
    nav_title = models.CharField(
        verbose_name="ナビゲーションのタイトル",
        default="アナリティクス",
        max_length=50,
        help_text="ナビゲーションバーの左上に表記される文字",
    )
    heading_ja = models.CharField(
        verbose_name="日本語の見出し",
        default="ようこそアナリティクスページへ",
        max_length=100,
        help_text="画面中央頭に表記される見出し。日本語で記入してください。",
    )
    heading_us = models.CharField(
        verbose_name="英語の見出し",
        default="Welcome to analytics page",
        max_length=100,
        help_text="画面中央頭に表記される見出し。英語で記入してください。",
    )
    base_html_file = models.CharField(
        blank=True,
        null=True,
        verbose_name="ベースファイル",
        default="base.html",
        max_length=100,
        help_text="htmlファイルのベースとなるファイル名を入力してください。プロジェクト直下の場合は「base.html」。アプリ直下の場合は「app/base.html」。",
    )
    container = models.CharField(
        verbose_name="コンテナ",
        blank=True,
        default="container",
        max_length=15,
        choices=CONTAINER_CHOICES,
    )
    col_left = models.PositiveIntegerField(
        verbose_name="カラム左側",
        default=2,
        validators=[MaxValueValidator(9)],
        help_text="デフォルト値は２です",
    )
    col_center = models.PositiveIntegerField(
        verbose_name="カラム中央",
        default=8,
        validators=[MinValueValidator(3), MaxValueValidator(12)],
        help_text="デフォルト値は８です",
    )
    col_right = models.PositiveIntegerField(
        verbose_name="カラム右側",
        default=2,
        validators=[MaxValueValidator(9)],
        help_text="デフォルト値は２です",
    )

    def save(self, *args, **kwargs):
        """テンプレートファイルのベースファイル設定"""
        import os
        import re

        basehtml_file = "templates/analytics/base_index.html"
        file_dir = os.path.join(os.path.dirname(__file__), basehtml_file)
        with open(file_dir) as f:
            html_text = f.read()

        existing_name = re.search("^" + self.base_html_file, html_text)
        if not existing_name:
            # 既存のベース.htmlが検索されなければ新名と置き換え
            # 正規表現モジュールを使ってベースファイル名を置き換える
            comp = re.compile(r"extends \'\w+.html|extends \'\w+/\w+.html")
            html_text = comp.sub("extends '" + self.base_html_file, html_text)

            with open(file_dir, "w") as f:
                f.write(html_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nav_title

    class Meta:
        verbose_name = "アナリティクスアプリの設定"
        verbose_name_plural = "アナリティクスアプリの設定"


class GoogleAnalytics4Config(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        verbose_name="作成者",
        on_delete=models.CASCADE,
    )
    property_id = models.CharField(verbose_name="プロパティID", max_length=150)
    days_ago = models.PositiveIntegerField(
        verbose_name="日付の範囲",
        default=7,
        validators=[MaxValueValidator(30)],
    )

    def save(self, *args, **kwargs):
        # 保存する前にプロパティIDの暗号化
        try:
            self.property_id = encryption(self.property_id)
        except ValueError:
            # 既に暗号化されている場合は一度復号化してから再度暗号化して保存
            self.property_id = encryption(decryption(self.property_id))
        super().save(*args, **kwargs)

    def __str__(self):
        author = str(self.author)
        return author

    class Meta:
        verbose_name = "Googleアナリティクス4の構成"
        verbose_name_plural = "Googleアナリティクス4の構成"


class DimensionDate(models.Model):
    dates = models.DateField(verbose_name="日付")  # 西暦と月日を保存
    users = models.PositiveIntegerField(verbose_name="アクセス数")  # 0と正の整数を保存
    new_users = models.PositiveIntegerField(verbose_name="新規ユーザー数")
    page_views = models.PositiveIntegerField(verbose_name="ページビュー数")
    sessions = models.PositiveIntegerField(verbose_name="セッション数")
    ad_revenue = models.PositiveIntegerField(verbose_name="広告収益")
    ad_impressions = models.PositiveIntegerField(verbose_name="インプレッション数")

    def __str__(self):
        dates = str(self.dates)
        return dates

    class Meta:
        verbose_name = "アナリティクスデータ"
        verbose_name_plural = "アナリティクスデータ"


# Create your models here.
