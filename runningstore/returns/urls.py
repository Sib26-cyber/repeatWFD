from django.urls import path
from . import views

app_name = "returns"

urlpatterns = [
    path("my/", views.my_returns, name="my_returns"),
    path("create/", views.create_return_request, name="create"),

    path("queue/", views.queue, name="queue"),
    path("approve/", views.approve_return, name="approve"),
    path("reject/", views.reject_return, name="reject"),
    path("received/", views.mark_received, name="received"),
    path("refund/", views.mock_refund, name="refund"),
]