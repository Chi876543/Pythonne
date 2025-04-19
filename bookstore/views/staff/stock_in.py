from django.shortcuts import render, redirect
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