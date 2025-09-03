from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db import transaction

# If your app is named "payments" use: from payments.models import Order, OrderItem
from payment.models import Order, OrderItem

from .models import ReturnRequest, ReturnStatus, Refund
from .forms import ReturnRequestForm, StaffDecisionForm


@login_required
def create_return_request(request):
    """
    Flat URL style:
      - GET  /returns/create/?order=<id>  -> show form for that order
      - POST /returns/create/ with fields: order_id, order_item, reason, requested_amount
    """
    # Resolve order from querystring (GET) or hidden field (POST)
    order_id = request.GET.get("order") or request.POST.get("order_id")
    if not order_id:
        return HttpResponseBadRequest("Missing order id.")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        form = ReturnRequestForm(request.POST)
        # Limit choices to this order's items before validating
        form.fields["order_item"].queryset = OrderItem.objects.filter(order=order)
        if form.is_valid():
            rr = form.save(commit=False)
            # extra safety: ensure the selected item belongs to this order
            if rr.order_item.order_id != order.id:
                return HttpResponseBadRequest("Selected item does not belong to this order.")
            rr.order = order
            rr.requested_by = request.user
            rr.save()
            messages.success(request, "Return request submitted.")
            return redirect("returns:my_returns")
    else:
        form = ReturnRequestForm()
        form.fields["order_item"].queryset = OrderItem.objects.filter(order=order)

    return render(request, "returns/create.html", {"order": order, "form": form})


@login_required
def my_returns(request):
    qs = (
        ReturnRequest.objects
        .filter(requested_by=request.user)
        .select_related("order", "order_item")
        .order_by("-created_at")
    )
    return render(request, "returns/my_returns.html", {"returns": qs})


# ---------- Staff actions (flat URLs, IDs via POST) ----------

@require_POST
@permission_required("returns.change_returnrequest")
@transaction.atomic
def approve_return(request):
    rr_id = request.POST.get("return_id")
    if not rr_id:
        return HttpResponseBadRequest("Missing return_id.")
    rr = get_object_or_404(ReturnRequest, id=rr_id)

    form = StaffDecisionForm(request.POST, instance=rr)
    if form.is_valid():
        rr = form.save(commit=False)
        rr.status = ReturnStatus.APPROVED
        rr.save()
        messages.success(request, f"Return #{rr.id} approved.")
    else:
        messages.error(request, "Invalid data for approval.")
    return redirect("returns:queue")


@require_POST
@permission_required("returns.change_returnrequest")
@transaction.atomic
def reject_return(request):
    rr_id = request.POST.get("return_id")
    if not rr_id:
        return HttpResponseBadRequest("Missing return_id.")
    rr = get_object_or_404(ReturnRequest, id=rr_id)

    # allow staff to optionally set approved_amount to 0 via same form
    form = StaffDecisionForm(request.POST, instance=rr)
    if form.is_valid():
        rr = form.save(commit=False)
        rr.status = ReturnStatus.REJECTED
        rr.save()
        messages.success(request, f"Return #{rr.id} rejected.")
    else:
        messages.error(request, "Invalid data for rejection.")
    return redirect("returns:queue")


@require_POST
@permission_required("returns.change_returnrequest")
def mark_received(request):
    rr_id = request.POST.get("return_id")
    if not rr_id:
        return HttpResponseBadRequest("Missing return_id.")
    rr = get_object_or_404(ReturnRequest, id=rr_id, status=ReturnStatus.APPROVED)
    rr.status = ReturnStatus.RECEIVED
    rr.save(update_fields=["status"])
    messages.success(request, f"Return #{rr.id} marked as received.")
    return redirect("returns:queue")


@require_POST
@permission_required("returns.change_refund")
@transaction.atomic
def mock_refund(request):
    rr_id = request.POST.get("return_id")
    if not rr_id:
        return HttpResponseBadRequest("Missing return_id.")
    rr = get_object_or_404(
        ReturnRequest,
        id=rr_id,
        status__in=[ReturnStatus.APPROVED, ReturnStatus.RECEIVED],
    )

    amount = rr.approved_amount or rr.requested_amount
    refund, created = Refund.objects.get_or_create(
        order=rr.order,
        return_request=rr,
        defaults={"amount": amount, "reason": rr.reason, "processed": True},
    )
    if not created and not refund.processed:
        refund.amount = amount
        refund.processed = True
        refund.save(update_fields=["amount", "processed"])

    rr.refunded_amount = amount
    rr.status = ReturnStatus.REFUNDED
    rr.save(update_fields=["refunded_amount", "status"])

    # Optional: restock inventory based on rr.order_item.quantity
    # product = rr.order_item.product
    # product.stock = product.stock + rr.order_item.quantity
    # product.save(update_fields=["stock"])

    messages.success(request, f"Refund recorded for return #{rr.id}.")
    return redirect("returns:queue")


@permission_required("returns.change_returnrequest")
def queue(request):
    pending = (
        ReturnRequest.objects
        .filter(status=ReturnStatus.REQUESTED)
        .select_related("order", "order_item", "requested_by")
        .order_by("created_at")
    )
    return render(request, "returns/queue.html", {"pending": pending})