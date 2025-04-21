from django.shortcuts import render, redirect
from ...models import Book, StockOut, OrderDetail, Order
def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_stock_out(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')
    stock_outs = StockOut.objects.all()
    
    return render(request, 'staff/stock_out/stock_out_list.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
        'stock_outs': stock_outs,
    })
