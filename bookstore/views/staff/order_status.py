# admin.py
from django.shortcuts import render, redirect, get_object_or_404
from ...models import Order, User, OrderDetail, StockOut    
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta

def can_view_order(user):
    return user.has_perm('bookstore.can_view_order')

def can_change_order(user):
    return user.has_perm('bookstore.can_change_order')

# def can_view_order_detail(user):
#     return user.has_perm('bookstore.can_view_orderdetail')

@login_required
@user_passes_test(can_view_order)
def admin_list_orders(request):
    orders = Order.objects.all()  
    users = User.objects.all()  # Lấy tất cả người dùng
    customer_filter = request.GET.get('customer_name')
    address_filter = request.GET.get('address')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    if start_date_filter and end_date_filter:
        start_date = datetime.strptime(start_date_filter, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_filter, "%Y-%m-%d") + timedelta(days=1)
        orders = orders.filter(created_at__gte=start_date, created_at__lt=end_date)
    if customer_filter:
        orders = orders.filter(user__full_name__icontains=customer_filter)
    if address_filter:
        orders = orders.filter(address__icontains=address_filter)
    return render(request, 'staff/order/order_list.html', {
        'users': users,
        'orders': orders,  
        'customer_filter': customer_filter,
        'address_filter': address_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'status_filter': status_filter,
    })



@login_required
@user_passes_test(can_change_order)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    current_status = order.status
    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status == "Completed" and current_status != "Confirmed":
            messages.warning(request, "⚠️ Chỉ được chuyển sang Completed nếu đơn hàng đang ở trạng thái Confirmed.")
            return redirect('list_order')

        order.status = new_status
        order.save()
        for detail in order.orderdetail_set.all():
            if new_status == "Completed":  # Chỉ giảm stock khi chuyển sang trạng thái Completed
                detail.book.stock -= detail.quantity
                detail.book.save()

        if new_status == "Confirmed":
            if not StockOut.objects.filter(order=order).exists():
                for detail in order.orderdetail_set.all():
                    StockOut.objects.create(
                        order=order,
                        book=detail.book,
                        quantity=detail.quantity,
                        date=timezone.now(),
                        note=f"Xuất kho cho đơn hàng #{order.id}"
                    )

        messages.success(request, f"✅ Đã cập nhật trạng thái đơn hàng #{order.id} thành '{new_status}'")
        return redirect('list_order')

        
    return render(request, 'staff/order/order_list.html')
@login_required
def admin_order_detail(request, order_id):
    order_detail = OrderDetail.objects.filter(order_id=order_id)
    for detail in order_detail:
        detail.total_price = detail.price * detail.quantity
    return render(request, 'staff/order/order_detail.html', {
        'order_detail': order_detail,
    })