from django.shortcuts import render, redirect
from ...models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def can_view_user(user):
    return user.has_perm('bookstore.can_view_user')

def can_add_user(user):
    return user.has_perm('bookstore.can_add_user')

@login_required
@user_passes_test(can_view_user)
def admin_list_users(request):
    role_filter = request.GET.get('role')
    if role_filter:
        users = User.objects.filter(role=role_filter)
    else:
        users = User.objects.all()
    
    context = {
        'roles': User.ROLE_CHOICES,
        'users': users,
        'role_filter': role_filter
    }

    return render(request, 'admin/user/user_list.html', context)

@login_required
@user_passes_test(can_add_user)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        status = request.POST.get('status')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on' 

        user = User.objects.create_user(username=username, password=password, email=email)
        user.phone = phone
        user.full_name = full_name 
        user.role = role
        user.address = address
        user.status = status
        user.is_staff = is_staff 
        user.is_superuser = is_superuser  
        user.save()

        messages.success(request, 'Người dùng đã được thêm thành công!')
        return redirect('list_user') 

    return render(request, 'admin/user/add_user.html')