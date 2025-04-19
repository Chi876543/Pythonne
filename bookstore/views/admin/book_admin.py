from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_list_books(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để lấy danh sách sách từ cơ sở dữ liệu
    # books = Book.objects.all()  # Giả sử bạn có một mô hình Book

    return render(request, 'admin/book/list_book.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
    })