from django.shortcuts import render
from ...models import Book, Category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

@login_required
@user_passes_test(can_view_group)
def admin_list_books(request):
    category_filter = request.GET.get('category_name', '')
    search_filter = request.GET.get('search_book', '')
    books = Book.objects.all()
    if category_filter:
        books = books.filter(category_id=category_filter)
    if search_filter:
        books = books.filter(
            Q(title__icontains=search_filter) | Q(author__icontains=search_filter)
        )
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'books': books,
        'category_name': category_filter,
        'search_book': search_filter,
        }

    return render(request, 'admin/book/list_book.html', context)