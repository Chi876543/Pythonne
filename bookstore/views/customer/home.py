# bookstore/views/customer/home.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from ...models import Book

def home(request):
    return render(request, 'customer/home.html')

def books(request):
    # Lấy danh sách sách
    books = Book.objects.filter(status='available')

    # Tìm kiếm sách
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # Phân trang (10 sách mỗi trang)
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Chuẩn bị dữ liệu JSON
    books_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock': book.stock,
            'imagePath': book.imagePath.url if book.imagePath else None,
        }
        for book in page_obj
    ]

    # Trả về JSON
    return JsonResponse({
        'books': books_data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })