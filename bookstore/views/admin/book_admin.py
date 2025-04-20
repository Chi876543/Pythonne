from django.shortcuts import render
from ...models import Book, Category
from django.contrib.auth.decorators import login_required, user_passes_test

def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

@login_required
@user_passes_test(can_view_group)
def admin_list_books(request):
    category_filter = request.GET.get('category_name', '')
    title_filter = request.GET.get('title', '')
    author_filter = request.GET.get('author', '')
    books = Book.objects.all()
    if category_filter:
        books = books.filter(category_id=category_filter)
    if title_filter:
        books = books.filter(title__icontains=title_filter)
    if author_filter:
        books = books.filter(author__icontains=author_filter)
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'books': books,
        'category_name': category_filter,
        'title': title_filter,
        'author': author_filter,
    }

    return render(request, 'admin/book/list_book.html', context)