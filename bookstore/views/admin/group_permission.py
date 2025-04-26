from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.contrib import messages

def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

def can_add_group(user):
    return user.has_perm('bookstore.can_add_group')

def can_delete_group(user):
    return user.has_perm('bookstore.can_delete_group')

def can_change_group(user):
    return user.has_perm('bookstore.can_change_group')

@login_required
# @user_passes_test(can_view_group)
def admin_list_group(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_permission/list_group.html', {'groups': groups})

@login_required
# @user_passes_test(can_add_group)
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

@login_required
# @user_passes_test(can_change_group)
def change_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)  # Get the group by ID

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        permissions = request.POST.getlist('permissions')

        group.name = group_name  # Update the group name
        group.permissions.clear()  # Clear existing permissions

        for perm_id in permissions:
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)  # Add new permissions

        group.save()  # Save the updated group
        messages.success(request, 'Cập nhật nhóm thành công.')
        return redirect('list_group')

    permissions = Permission.objects.all()
    # Prepare a list of permission IDs for the current group
    group_permission_ids = list(group.permissions.values_list('id', flat=True))  # Convert to a list

    context = {
        'group': group,
        'permissions': permissions,
        'group_permission_ids': group_permission_ids  # Pass the list to the template
    }
    
    return render(request, 'admin/group_permission/change_group.html', context)

@login_required
# @user_passes_test(can_delete_group)
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)  # Get the group by ID

    if request.method == 'POST':
        group.delete()  # Delete the group
        messages.success(request, 'Xóa nhóm thành công.')
        return redirect('list_group')

    context = {
        'group': group
    }
    
    return render(request, 'admin/group_permission/delete_group.html', context)