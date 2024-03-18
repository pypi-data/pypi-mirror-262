from django.contrib.auth import views as auth_views  # type: ignore
from django.urls import path  # type: ignore

from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("pulldown/", views.pulldown, name="pulldown"),
    path("update/", views.Update.as_view(), name="update"),
    path("accounts/login/", auth_views.LoginView.as_view()),
]
