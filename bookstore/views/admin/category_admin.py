from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ...models import Category

def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

@login_required
@user_passes_test(can_view_group)
def admin_list_category(request):
    """
    View function to list all categories in the admin panel.
    """
    categories = Category.objects.all()
    category_name = request.GET.get('category_name', '')
    if category_name:
        categories = categories.filter(name__icontains=category_name)
    context ={
        'categories': categories,
        'category_name': request.GET.get('category_name', ''),
    }
    return render(request, 'admin/category/list_category.html',context)