# admin.py
from django.shortcuts import render, redirect
def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_list_orders(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để lấy danh sách đơn hàng từ cơ sở dữ liệu
    # orders = Order.objects.all()  # Giả sử bạn có một mô hình Order

    return render(request, 'staff/order/order_list.html', {
        'user': request.user,
        # 'orders': orders,  # Truyền danh sách đơn hàng vào template
    })

