from django.contrib import messages  # type: ignore
from django.contrib.auth.mixins import UserPassesTestMixin  # type: ignore
from django.http import JsonResponse  # type: ignore
from django.shortcuts import redirect, render  # type: ignore
from django.views.generic.base import View  # type: ignore
from django_pandas.io import read_frame  # type: ignore

from .models import AnalyticsAppSettings, DimensionDate, GoogleAnalytics4Config
from .update_api import update_data


class HomePageView(View):
    def get(self, request):
        context: dict = {}
        try:
            analytics_set = AnalyticsAppSettings.objects.all().last()
            dd_obj_all = DimensionDate.objects.all()
            # 値が存在するか
            dd_value_exist = dd_obj_all.exists()
            if dd_value_exist:
                # 値が存在すればデータフレームを作成する --------------------------
                df = read_frame(DimensionDate.objects.all())
                # 日付データを「年月」のフォーマットに変換
                df["dates"] = df["dates"].apply(lambda df: df.strftime("%Y年%m月"))
                # 日付データを元に日付以外のデータを集約する
                df = df.drop("id", axis=1).groupby(df["dates"]).sum()
                # テーブルに渡す用に、日付を降順にソートしたデータフレームを作成
                df_descending = df.sort_values("dates", ascending=False)
                # テンプレートへ渡すコンテキストデータに格納
                context["data_graph"] = df
                context["data_graph_subtitle"] = f"{df.index[0]} - {df.index[-1]}"
                context["data_table"] = df_descending
            context["analytics_set"] = analytics_set
            context["dd_exist"] = dd_value_exist
            template = "analytics/base_index.html"
            return render(request, template, context)
        except Exception as inst:
            Exception(inst)
            return render(request, "analytics/index.html", context)


def pulldown(request):
    """セレクトフォームによる非同期処理"""
    data_name = request.GET.get("data_name")
    date_value = request.GET.get("date_value")
    dd_obj_all = DimensionDate.objects.all()

    # フィールドのバーボスネーム取得
    for field in dd_obj_all.first()._meta.get_fields():
        if field.name == data_name:
            verbose_name = field.verbose_name

    df = read_frame(dd_obj_all)
    # 日付データを「年月」のフォーマットに変換
    df["dates"] = df["dates"].apply(lambda df: df.strftime("%Y年%m月"))
    # 日付データを元に日付以外のデータを集約する
    df = df.drop("id", axis=1).groupby(df["dates"]).sum()

    # グラフ用の処理 ----------------------------------------------
    # 日付の設定値を変える処理
    if date_value == "2":
        df = df[-12:]
    elif date_value == "3":
        df = df[-6:]

    if not request.user.is_staff:
        df.drop(["ad_revenue", "ad_impressions"], axis=1, inplace=True)

    # jsresponse用にリストを作成
    graph_data = [[index, data] for index, data in zip(df.index, df[data_name])]

    # テーブル用の処理 ---------------------------------------------
    # テーブルに渡す用に、日付を降順にソートしたデータフレームを作成
    df_descending = df.sort_values("dates", ascending=False)

    # # 日付の設定値を変える処理
    # if date_value == "2":
    #     df_descending = df_descending[:12]
    # elif date_value == "3":
    #     df_descending = df_descending[:6]

    # if not request.user.is_staff:
    #     df_descending.drop(["ad_revenue", "ad_impressions"], axis=1, inplace=True)

    # jsresponse用にリストを作成
    ls_data = [
        [index, data]
        for index, data in zip(df_descending.index, df_descending[data_name])
    ]

    return JsonResponse(
        {
            "data_table_head": verbose_name,
            "data_table": ls_data,
            "data_graph": graph_data,
        },
        status=200,
    )


class Update(UserPassesTestMixin, View):
    raise_exception = True

    def get(self, request):
        """アナリティクスデータの更新"""
        try:
            ga4_config = GoogleAnalytics4Config.objects.all().first()
            update_data.update_analyticsdata(ga4_config)
            messages.success(request, "アナリティクスデータの更新が完了しました")
            return redirect("analytics:index")
        except Exception:
            messages.error(request, "GoogleAnalytics4Configの設定ができていません")
            return redirect("analytics:index")

    def test_func(self):
        # スタッフユーザーでなければ４０３ページ
        return self.request.user.is_staff
