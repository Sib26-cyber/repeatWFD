from django.urls import path
from . import views

app_name = "returns"

urlpatterns = [
    path("my/", views.my_returns, name="my_returns"),
    path("<int:order_id>/new/", views.create_return_request, name="create"),
    path("staff/queue/", views.queue, name="queue"),
    path("staff/<int:pk>/approve/", views.approve_or_reject, name="approve"),
    path("staff/<int:pk>/received/", views.mark_received, name="received"),
    path("staff/<int:pk>/refund/", views.mock_refund, name="refund"),
]