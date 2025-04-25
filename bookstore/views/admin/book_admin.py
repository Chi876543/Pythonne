from django.shortcuts import render, redirect, get_object_or_404
from ...models import Book, Category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

def can_add_book(user):
    return user.has_perm('bookstore.can_add_book')

def can_view_books(user):
    return user.has_perm('bookstore.can_view_books')

def can_change_book(user):
    return user.has_perm('bookstore.can_change_book')

@login_required
@user_passes_test(can_view_books)
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

@login_required
@user_passes_test(can_add_book)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        if 'imagePath' in request.FILES:
            image = request.FILES['image']
        else:
            image = 'book_images/default.png' 

        book = Book(
            title=title,
            author=author,
            price=price,
            stock=stock,
            status=status,
            category_id=category_id,
            description=description,
            imagePath=image  
        )
        book.save()

        messages.success(request, 'Sách đã được thêm thành công!')
        return redirect('list_book') 
    categories = Category.objects.all()
    return render(request, 'admin/book/add_book.html', {'categories': categories})

@login_required
@user_passes_test(can_change_book)
def change_book(request, book_id):
    # Lấy sách theo ID
    book = get_object_or_404(Book, id=book_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Manually handle form data
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.stock = request.POST.get('stock')
        book.status = request.POST.get('status')
        book.category_id = request.POST.get('category')
        book.description = request.POST.get('description')

        if 'imagePath' in request.FILES:
            book.imagePath = request.FILES['imagePath'] 

        book.save()
        messages.success(request, 'Sách đã được cập nhật thành công!')
        return redirect('list_book')
    
    return render(request, 'admin/book/change_book.html', {'book': book, 'categories': categories})