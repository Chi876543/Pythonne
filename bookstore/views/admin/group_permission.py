from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required
def admin_list_group(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_permission/list_group.html', {'groups': groups})