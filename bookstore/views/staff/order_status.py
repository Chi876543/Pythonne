# admin.py
from django.shortcuts import render, redirect
from ...models import Order, User
def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_list_orders(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    orders = Order.objects.all()  
    users = User.objects.all()  # Lấy tất cả người dùng
    return render(request, 'staff/order/order_list.html', {
        'users': users,
        'orders': orders,  
    })
def admin_order_detail(request, order_id):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    order = Order.objects.get(id=order_id)  
    users = User.objects.all()  # Lấy tất cả người dùng
    return render(request, 'staff/order/order_detail.html', {
        'users': users,
        'order': order,  
    })
