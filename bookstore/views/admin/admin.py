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
        return admin_dashboard(request)

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

def admin_dashboard(request):
    user = request.user
    content = {
        "can_view_books": user.has_perm('bookstore.view_book'),                             # Kiểm tra xem user có quyền xem sách không
        #"can_add_book": user.has_perm('bookstore.add_book'),
        #"can_change_book": user.has_perm('bookstore.change_book'),
        #"can_delete_book": user.has_perm('bookstore.delete_book'),
        "can_view_orders": user.has_perm('bookstore.view_order'),                           # Kiểm tra xem user có quyền xem đơn hàng không
        #"can_add_order": user.has_perm('bookstore.add_order'),
        #"can_change_order": user.has_perm('bookstore.change_order'),
        #"can_delete_order": user.has_perm('bookstore.delete_order'),
        "can_view_categories": user.has_perm('bookstore.view_category'),                    # Kiểm tra xem user có quyền xem danh mục sách không  
        #"can_add_category": user.has_perm('bookstore.add_category'),
        #"can_change_category": user.has_perm('bookstore.change_category'),
        #"can_delete_category": user.has_perm('bookstore.delete_category'),
        "can_view_stockin": user.has_perm('bookstore.view_stockin'),                        # Kiểm tra xem user có quyền xem phiếu nhập không
        #"can_add_stockin": user.has_perm('bookstore.add_stockin'),
        #"can_change_stockin": user.has_perm('bookstore.change_stockin'),
        #"can_delete_stockin": user.has_perm('bookstore.delete_stockin'),
        "can_view_stockout": user.has_perm('bookstore.view_stockout'),                      # Kiểm tra xem user có quyền xem phiếu xuất không
        #"can_add_stockout": user.has_perm('bookstore.add_stockout'),
        #"can_change_stockout": user.has_perm('bookstore.change_stockout'),
        #"can_delete_stockout": user.has_perm('bookstore.delete_stockout'),
        "can_view_report": user.has_perm('bookstore.view_report'),                          # Kiểm tra xem user có quyền xem báo cáo không
        #"can_add_report": user.has_perm('bookstore.add_report'),
        #"can_change_report": user.has_perm('bookstore.change_report'),
        #"can_delete_report": user.has_perm('bookstore.delete_report'),
        "can_view_users": user.has_perm('auth.view_user'),                                  # Kiểm tra xem user có quyền xem user không
        #"can_add_user": user.has_perm('bookstore.add_user'),
        #"can_change_user": user.has_perm('bookstore.change_user'),
        #"can_delete_user": user.has_perm('bookstore.delete_user'),
    }
    return render(request, 'admin/admin_base.html', content)
