from django.shortcuts import render, redirect
from ...models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def can_view_user(user):
    return user.has_perm('bookstore.can_view_user')

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
