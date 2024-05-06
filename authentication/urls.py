from django.urls import path

from authentication.views import SignInView

app_name = "authentication"

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
]
