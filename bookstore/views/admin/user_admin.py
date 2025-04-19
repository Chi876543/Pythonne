from django.shortcuts import render, redirect
from ...models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def can_view_user(user):
    return user.has_perm('bookstore.can_view_user')

@login_required
@user_passes_test(can_view_user)
def admin_list_users(request):
   
    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'admin/user/user_list.html', context)