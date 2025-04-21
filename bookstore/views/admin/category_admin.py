from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ...models import Category
from django.contrib import messages

def can_view_category(user):
    return user.has_perm('bookstore.can_view_category')

def can_add_category(user):
    return user.has_perm('bookstore.can_add_category')

@login_required
@user_passes_test(can_view_category)
def admin_list_category(request):
    categories = Category.objects.all()

    category_name = request.GET.get('category_name', '')

    if category_name:
        categories = categories.filter(name__icontains=category_name)
    context ={
        'categories': categories,
        'category_name': request.GET.get('category_name', ''),
    }
    return render(request, 'admin/category/list_category.html',context)

@login_required
@user_passes_test(can_add_category)
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        category = Category(
            name=category_name,
        )
        category.save()

        messages.success(request, 'Thêm danh mục thành công.')
        return redirect('list_category')
    
    return render(request, 'admin/category/add_category.html')