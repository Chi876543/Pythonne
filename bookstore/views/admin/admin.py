from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login


def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin/admin_base.html')

def admin_login_view(request):
    return render(request, 'admin/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def admin_login(request):
    # Nếu đã đăng nhập và là admin → render dashboard
    if request.user.is_authenticated and is_admin(request.user):
        return render(request, 'admin/admin_base.html', {
            'user': request.user
        })

    # Nếu chưa đăng nhập và gửi form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and is_admin(user):
            auth_login(request, user)
            return redirect('admin_login') 
        else:
            return render(request, 'admin/login.html', {'error': 'Sai tài khoản hoặc không có quyền'})

    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    user = request.user
    content = {
        "can_view_users": user.has_perm('auth.view_user'),
        "can_add_user": user.has_perm('bookstore.add_user'),
        "can_change_user": user.has_perm('bookstore.change_user'),
        "can_delete_user": user.has_perm('bookstore.delete_user'),
        "can_view_books": user.has_perm('bookstore.view_book'),
        "can_add_book": user.has_perm('bookstore.add_book'),
        "can_change_book": user.has_perm('bookstore.change_book'),
        "can_delete_book": user.has_perm('bookstore.delete_book'),

    }
    return render(request, 'admin/admin_base.html', content)
