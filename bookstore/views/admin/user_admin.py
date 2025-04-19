from django.shortcuts import render, redirect
def is_admin(user):
    return user.is_authenticated and user.is_staff
def admin_list_users(request):
    # Chỉ admin mới có quyền truy cập
    if not is_admin(request.user):
        return redirect('admin_login')

    # Xử lý logic để lấy danh sách người dùng từ cơ sở dữ liệu
    # users = User.objects.all()  # Giả sử bạn có một mô hình User

    return render(request, 'admin/user/user_list.html', {
        'user': request.user,
        # 'users': users,  # Truyền danh sách người dùng vào template
    })