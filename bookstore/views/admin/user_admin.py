from django.shortcuts import render, redirect
from ...models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group, Permission

def can_view_user(user):
    return user.has_perm('bookstore.can_view_user')

def can_add_user(user):
    return user.has_perm('bookstore.can_add_user')

def can_change_user(user):
    return user.has_perm('bookstore.can_change_user')

@login_required
@user_passes_test(can_view_user)
def admin_list_users(request):
    role_filter = request.GET.get('role')
    is_staff_filter = request.GET.get('is_staff')
    is_superuser_filter = request.GET.get("is_superuser")
    full_name_filter = request.GET.get("full_name")
    users = User.objects.all()
    if full_name_filter:
        users = users.filter(full_name__icontains=full_name_filter)
    if role_filter:
        users = users.filter(role=role_filter)
    if is_staff_filter:
        users = users.filter(is_staff = is_staff_filter)
    if is_superuser_filter:
        users = users.filter(is_active = is_superuser_filter)
    context = {
        'roles': User.ROLE_CHOICES,
        'users': users,
        'role_filter': role_filter,
        'is_staff_filter': is_staff_filter,
        'is_superuser_filter': is_superuser_filter,
        'full_name_filter': full_name_filter,
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
        group_ids = request.POST.getlist('group')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.phone = phone
        user.full_name = full_name 
        user.role = role
        user.address = address
        user.status = status
        user.is_staff = is_staff 
        user.is_superuser = is_superuser  
        user.save()

        for group_id in group_ids:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)

        messages.success(request, 'Người dùng đã được thêm thành công!')
        return redirect('list_user') 
    
    groups = Group.objects.all()
    return render(request, 'admin/user/add_user.html', {'groups': groups})

@login_required
@user_passes_test(can_change_user)
def change_user(request, user_id):
    user = User.objects.get(id=user_id)  

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
        group_ids = request.POST.getlist('group')  

        user.username = username
        user.email = email
        user.full_name = full_name
        user.phone = phone
        user.address = address
        user.role = role
        user.status = status
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        if password:
            user.set_password(password)

        user.save() 

        user.groups.clear()
        for group_id in group_ids:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)

        messages.success(request, 'Người dùng đã được cập nhật thành công!')
        return redirect('list_user')

    groups = Group.objects.all() 
    user_group_ids = user.groups.values_list('id', flat=True)  
    return render(request, 'admin/user/change_user.html', {'user': user, 'groups': groups, 'user_group_ids': user_group_ids})