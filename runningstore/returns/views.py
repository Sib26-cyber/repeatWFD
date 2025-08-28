from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest
from django.db import transaction

from payment.models import Order, OrderItem
from .models import ReturnRequest, ReturnStatus, Refund
from .forms import ReturnRequestForm, StaffDecisionForm

@login_required
def create_return_request(request, order_id):
    # The payments.Order has user FK; ensure it’s theirs
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            rr = form.save(commit=False)
            # Ensure chosen item belongs to this order
            if rr.order_item.order_id != order.id:
                return HttpResponseBadRequest("Selected item does not belong to this order.")
            rr.order = order
            rr.requested_by = request.user
            rr.save()
            return redirect("returns:my_returns")
    else:
        form = ReturnRequestForm()
        # Limit order_item choices to items from this order only
        form.fields["order_item"].queryset = OrderItem.objects.filter(order=order)

    return render(request, "returns/create.html", {"order": order, "form": form})

@login_required
def my_returns(request):
    qs = ReturnRequest.objects.filter(requested_by=request.user).select_related("order", "order_item")
    return render(request, "returns/my_returns.html", {"returns": qs})

# ---- Staff area ----
@permission_required("returns.change_returnrequest")
def queue(request):
    pending = ReturnRequest.objects.filter(status=ReturnStatus.REQUESTED).select_related("order", "order_item")
    return render(request, "returns/queue.html", {"pending": pending})

@permission_required("returns.change_returnrequest")
@transaction.atomic
def approve_or_reject(request, pk):
    rr = get_object_or_404(ReturnRequest, pk=pk)
    if request.method == "POST":
        form = StaffDecisionForm(request.POST, instance=rr)
        if form.is_valid():
            rr = form.save(commit=False)
            approve = "approve" in request.POST or form.cleaned_data.get("approve")
            rr.status = ReturnStatus.APPROVED if approve else ReturnStatus.REJECTED
            rr.save()
            return redirect("returns:queue")
    else:
        form = StaffDecisionForm(instance=rr)
    return render(request, "returns/approve.html", {"rr": rr, "form": form})

@permission_required("returns.change_returnrequest")
def mark_received(request, pk):
    rr = get_object_or_404(ReturnRequest, pk=pk, status=ReturnStatus.APPROVED)
    rr.status = ReturnStatus.RECEIVED
    rr.save()
    return redirect("returns:queue")

@permission_required("returns.change_refund")
@transaction.atomic
def mock_refund(request, pk):
    rr = get_object_or_404(ReturnRequest, pk=pk, status__in=[ReturnStatus.APPROVED, ReturnStatus.RECEIVED])
    amount = rr.approved_amount or rr.requested_amount

    refund, created = Refund.objects.get_or_create(
        order=rr.order,
        return_request=rr,
        defaults={"amount": amount, "reason": rr.reason, "processed": True},
    )
    if not created and not refund.processed:
        refund.amount = amount
        refund.processed = True
        refund.save()

    rr.refunded_amount = amount
    rr.status = ReturnStatus.REFUNDED
    rr.save()
    # Optional: restock based on rr.order_item.quantity
    return redirect("returns:queue")

