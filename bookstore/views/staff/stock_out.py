from django.shortcuts import render, redirect
from ...models import Book, StockOut, OrderDetail, Order
from django.contrib.auth.decorators import login_required, user_passes_test

def can_view_stockout(user):
    return user.has_perm('bookstore.can_view_stockout')

@login_required
@user_passes_test(can_view_stockout)
def admin_stock_out(request):
    stock_outs = StockOut.objects.all()
    
    return render(request, 'staff/stock_out/stock_out_list.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
        'stock_outs': stock_outs,
    })
