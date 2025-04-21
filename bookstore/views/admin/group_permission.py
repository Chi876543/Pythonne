from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.contrib import messages

def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

def can_add_group(user):
    return user.has_perm('bookstore.can_add_group')

@login_required
@user_passes_test(can_view_group)
def admin_list_group(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_permission/list_group.html', {'groups': groups})

@login_required
@user_passes_test(can_add_group)
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        permissions = request.POST.getlist('permissions')

        group = Group.objects.create(name=group_name)

        for perm_id in permissions:
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)

        messages.success(request, 'Thêm nhóm thành công.')
        return redirect('list_group')
    
    perm = Permission.objects.all
    context = {
        'permissions': perm
    }
    
    return render(request, 'admin/group_permission/add_group.html', context)