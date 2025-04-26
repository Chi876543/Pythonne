from django.shortcuts import render, redirect
from ...models import Book, StockOut, OrderDetail, Order
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
def can_view_stockout(user):
    return user.has_perm('bookstore.can_view_stockout')

@login_required
# @user_passes_test(can_view_stockout)
def admin_stock_out(request):
    stock_outs = StockOut.objects.all()
    order_id_filter = request.GET.get('order_id', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    if order_id_filter:
        stock_outs = StockOut.objects.filter(order__id=order_id_filter)
    if start_date_filter and end_date_filter:
        start_date = datetime.strptime(start_date_filter, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_filter, "%Y-%m-%d") + timedelta(days=1)

        stock_outs = stock_outs.filter(date__gte=start_date, date__lt=end_date)
    for stock_out in stock_outs:
    # Tìm OrderDetail khớp với order và book
        order_detail = OrderDetail.objects.filter(order=stock_out.order, book=stock_out.book).first()
        if order_detail:
            stock_out.price = order_detail.price
            stock_out.total_price = order_detail.price * stock_out.quantity
        else:
            stock_out.price = 0
            stock_out.total_price = 0    
    return render(request, 'staff/stock_out/stock_out_list.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
        'stock_outs': stock_outs,
        'order_id_filter': order_id_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    })
