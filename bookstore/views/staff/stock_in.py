from django.shortcuts import render, redirect
from ...models import Book, StockIn
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseBadRequest  

def can_view_stockin(user):
    return user.has_perm('bookstore.can_view_stockin')

def can_add_stockin(user):
    return user.has_perm('bookstore.can_add_stockin')

def is_admin(user):
    return user.is_authenticated and user.is_staff
def admin_stock_in(request):
    # if not is_admin(request.user):
    #     return redirect('admin_login')
    book_filter = request.GET.get('book_name')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    books = Book.objects.all()  # Giả sử bạn có một mô hình Book
    return render(request, 'staff/stock_in/stock_in_list.html', {
        'user': request.user,
        'books': books,  # Truyền danh sách sách vào template
    })

@login_required
@user_passes_test(can_add_stockin)
def add_stockin(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        note = request.POST.get('note')

        stockin = StockIn(
            quantity=quantity,
            date=date,
            note=note,
            book_id=book_id
        )
        stockin.save()

        messages.success(request, 'Phiếu nhập đã được thêm thành công!')
        return redirect('list_stock_in') 
    
    books = Book.objects.all()
    return render(request, 'staff/stock_in/add_stock_in.html', {'books': books})