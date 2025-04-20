from django.shortcuts import render, redirect
from ...models import Book, StockIn
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def can_view_stockin(user):
    return user.has_perm('bookstore.can_view_stockin')

def can_add_stockin(user):
    return user.has_perm('bookstore.can_add_stockin')

def is_admin(user):
    return user.is_authenticated and user.is_staff
def admin_stock_in(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để lấy danh sách sách từ cơ sở dữ liệu
    # books = Book.objects.all()  # Giả sử bạn có một mô hình Book

    return render(request, 'staff/stock_in/stock_in_list.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
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