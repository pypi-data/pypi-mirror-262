from django.contrib.auth.models import User  # type: ignore
from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from django.utils.encoding import force_text  # type: ignore
from django_pandas.io import read_frame  # type: ignore

from analytics.models import DimensionDate


def create_dimensiondate():
    for i in range(2):
        date = timezone.now().date() - timezone.timedelta(days=i)
        DimensionDate.objects.create(
            dates=date,
            users=1,
            new_users=1,
            page_views=1,
            sessions=1,
            ad_revenue=1,
            ad_impressions=1,
        )


class HomePageViewTests(TestCase):
    """HomePageViewのテスト"""

    def setUp(self):
        self.cdd = create_dimensiondate()

    def tearDown(self):
        del self.cdd

    def test_not_analytics_data(self):
        """アナリティクスアプリの初期設定をしていない場合のページテスト"""
        # HomePageViewを編集して条件かなんかでindex.htmlを読み込ませる必要がある
        # url = reverse("analytics:index")
        # response = self.client.get(url)
        # template_name = "analytics/index.html"
        # self.assertTemplateUsed(response, template_name)

    def test_create_context_data(self):
        """データが存在した場合にコンテキストデータを作成するテスト"""
        df = read_frame(DimensionDate.objects.all())
        df["dates"] = df["dates"].apply(lambda df: df.strftime("%Y年%m月"))
        df = df.drop("id", axis=1).groupby(df["dates"]).sum()
        data_graph_subtitle = f"{df.index[0]} - {df.index[-1]}"
        df_descending = df.sort_values("dates", ascending=False)
        url = reverse("analytics:index")
        response = self.client.get(url)
        self.assertEqual(response.context["data_graph"].index[0], df.index[0])
        self.assertEqual(response.context["data_graph_subtitle"], data_graph_subtitle)
        self.assertEqual(response.context["data_table"].index[0], df_descending.index[0])


def create_json_data(data, *, is_staff=True):
    """JSONResponse用のデータを作成する
    引数「*」は、それより後の引数を位置引数として使わさず、
    キーワード引数として使用するように定める引数"""
    dd_obj_all = DimensionDate.objects.all()
    for field in dd_obj_all.first()._meta.get_fields():
        if field.name == data["data_name"]:
            verbose_name = field.verbose_name

    df = read_frame(dd_obj_all)
    df["dates"] = df["dates"].apply(lambda df: df.strftime("%Y年%m月"))
    df = df.drop("id", axis=1).groupby(df["dates"]).sum()
    if data["date_value"] == "2":
        df = df[-12:]
    elif data["date_value"] == "3":
        df = df[-6:]
    if not is_staff:
        df.drop(["ad_revenue", "ad_impressions"], axis=1, inplace=True)
    graph_data = [[index, data] for index, data in zip(df.index, df[data["data_name"]])]
    df_descending = df.sort_values("dates", ascending=False)
    ls_data = [
        [index, data]
        for index, data in zip(df_descending.index, df_descending[data["data_name"]])
    ]
    json_data = {
        "data_table_head": verbose_name,
        "data_table": ls_data,
        "data_graph": graph_data,
    }
    return json_data


class PulldownTests(TestCase):
    """Pulldownのテスト"""

    def setUp(self):
        self.admin_user = User.objects.create(
            username="myuser", is_superuser=True, is_staff=True
        )
        self.cdd = create_dimensiondate()

    def tearDown(self):
        del self.admin_user
        del self.cdd

    def test_pulldown_jsonresponse(self):
        """プルダウンでのjsonレスポンスのテスト"""

        self.client.force_login(self.admin_user)
        url = reverse("analytics:pulldown")
        data = {"data_name": "users", "date_value": "0"}
        json_data = create_json_data(data)
        response = self.client.get(url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response_content, json_data)

    def test_pulldown_jsonresponse_date_12month_edit(self):
        """プルダウンでのjsonレスポンスで日付が変更された際のテスト"""

        self.client.force_login(self.admin_user)
        url = reverse("analytics:pulldown")
        data = {"data_name": "users", "date_value": "2"}
        json_data = create_json_data(data)
        response = self.client.get(url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response_content, json_data)

    def test_pulldown_jsonresponse_date_6month_edit(self):
        """プルダウンでのjsonレスポンスで日付が変更された際のテスト"""

        self.client.force_login(self.admin_user)
        url = reverse("analytics:pulldown")
        data = {"data_name": "users", "date_value": "3"}
        json_data = create_json_data(data)
        response = self.client.get(url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response_content, json_data)

    def test_pulldown_jsonresponse_generaluser_access(self):
        """プルダウンでのjsonレスポンスで一般ユーザーがアクセスした際のテスト"""

        self.client.logout()
        url = reverse("analytics:pulldown")
        data = {"data_name": "users", "date_value": "0"}
        json_data = create_json_data(data, is_staff=False)
        response = self.client.get(url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response_content, json_data)


class UpdateTests(TestCase):
    """Updateビューのテスト"""

    def setUp(self):
        self.admin_user = User.objects.create(
            username="myuser", is_superuser=True, is_staff=True
        )

    def tearDown(self):
        del self.admin_user

    def test_not_analytics_set_update(self):
        """GA4の設定をしていない状態でアップデートした際のテスト"""

        self.client.force_login(self.admin_user)
        url = reverse("analytics:update")
        response = self.client.get(url)
        redirect_url = reverse("analytics:index")
        self.assertRedirects(response, redirect_url)
