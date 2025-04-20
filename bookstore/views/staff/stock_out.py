from django.shortcuts import render, redirect
def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_stock_out(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để lấy danh sách sách từ cơ sở dữ liệu
    # books = Book.objects.all()  # Giả sử bạn có một mô hình Book

    return render(request, 'staff/stock_out/stock_out_list.html', {
        'user': request.user,
        # 'books': books,  # Truyền danh sách sách vào template
    })
def add_stock_out(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để thêm phiếu xuất kho vào cơ sở dữ liệu
    if request.method == 'POST':
        # Lấy thông tin từ form và lưu vào cơ sở dữ liệu
        # book_id = request.POST.get('book_id')
        # quantity = request.POST.get('quantity')
        # book = Book.objects.get(id=book_id)
        # book.stock -= int(quantity)
        # book.save()
        return redirect('stock_out_list')

    return render(request, 'staff/stock_out/add_stock_out.html', {
        'user': request.user,
    })