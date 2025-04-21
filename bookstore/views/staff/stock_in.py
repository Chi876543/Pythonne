from django.shortcuts import render, redirect
from ...models import Book, StockIn
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime, timedelta
def can_view_stockin(user):
    return user.has_perm('bookstore.can_view_stockin')

def can_add_stockin(user):
    return user.has_perm('bookstore.can_add_stockin')

def admin_stock_in(request):
    # if not is_admin(request.user):
    #     return redirect('admin_login')
    book_filter = request.GET.get('book_name', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    stock_ins = StockIn.objects.all()
    books = Book.objects.all()  # Giả sử bạn có một mô hình Book
    if book_filter:
        stock_ins = StockIn.objects.filter(book__title__icontains=book_filter)

    if start_date_filter and end_date_filter:
        start_date = datetime.strptime(start_date_filter, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_filter, "%Y-%m-%d") + timedelta(days=1)

        stock_ins = stock_ins.filter(date__gte=start_date, date__lt=end_date)

    
    for stock_in in stock_ins:
        stock_in.total_price = stock_in.price * stock_in.quantity
    return render(request, 'staff/stock_in/stock_in_list.html', {
        'user': request.user,
        'books': books,  # Truyền danh sách sách vào template
        'stock_ins': stock_ins,
        'book_filter': book_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    })

@login_required
@user_passes_test(can_add_stockin)
def add_stockin(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        note = request.POST.get('note')
        price = request.POST.get('price')
        stockin = StockIn(
            quantity=quantity,
            date=date,
            note=note,
            book_id=book_id,
            price =price,
        )
        stockin.save()

        messages.success(request, 'Phiếu nhập đã được thêm thành công!')
        return redirect('list_stock_in') 
    
    books = Book.objects.all()
    return render(request, 'staff/stock_in/add_stock_in.html', {'books': books})