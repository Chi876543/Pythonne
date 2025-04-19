from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from ...models import Book, Category
from django.contrib.auth.decorators import login_required, user_passes_test

def can_view_group(user):
    return user.has_perm('bookstore.can_view_group')

@login_required
@user_passes_test(can_view_group)
def admin_list_books(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    category_dict = {category.id: category.name for category in categories}

    for book in books:
        book.category_name = category_dict.get(book.category_id)

    context = {
        'books': books,
    }

    return render(request, 'admin/book/list_book.html', context)