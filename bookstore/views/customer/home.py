from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from ...models import Book, User, Category
from django.views.decorators.csrf import csrf_exempt


def home(request):
    # Lấy sách có trạng thái 'available'
    books = Book.objects.filter(status='available')


    # Lấy top 5 sách bán chạy (theo số lượng tồn kho)
    best_sellers = Book.objects.filter(status='available').order_by('-stock')[:6]


    # Xác định sách mới (dựa trên ID lớn nhất)
    max_id = Book.objects.filter(status='available').aggregate(Max('id'))['id__max']
    books_with_new = []
    for book in books:
        book.is_new = book.id == max_id  # Đánh dấu sách có ID lớn nhất là "mới"
        books_with_new.append(book)


    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)


    # Lọc theo giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)


    # Lọc theo chữ cái đầu của tiêu đề
    first_letter = request.GET.get('first_letter')
    if first_letter:
        books = books.filter(title__istartswith=first_letter)


    # Sắp xếp
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'title_asc':
        books = books.order_by('title')
    elif sort == 'title_desc':
        books = books.order_by('-title')


    # Tìm kiếm
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


    # Phân trang
    paginator = Paginator(books, 12)  # 12 sách mỗi trang
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)


    categories = Category.objects.all()


    context = {
        'books': page_obj,
        'best_sellers': best_sellers,
        'categories': categories,
        'page_obj': page_obj,
        'query': query or '',
        'sort': sort or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'category_id': category_id or '',
        'first_letter': first_letter or '',
    }
    return render(request, 'customer/home.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, status='available')
    return render(request, 'customer/book_detail.html', {'book': book})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Thiếu tên đăng nhập hoặc mật khẩu'}, status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == 'active':
                django_login(request, user)
                request.session.set_expiry(86400)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'full_name': user.full_name,
                        'phone': user.phone,
                        'address': user.address,
                        'status': user.status
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': 'Tài khoản không hoạt động'}, status=400)
        return JsonResponse({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu'}, status=400)
    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ'}, status=400)


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        django_logout(request)
        request.session.flush()
        return JsonResponse({
            'success': True,
            'message': 'Đăng xuất thành công'
        })
    return JsonResponse({
        'success': False,
        'message': 'Phương thức không được phép'
    }, status=405)
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')


        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Tên đăng nhập đã tồn tại'
            })


        if email and User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Email đã được sử dụng'
            })


        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            full_name=full_name,
            phone=phone,
            address=address,
            role='customer',
            status='active'
        )
        return JsonResponse({
            'success': True,
            'message': 'Đăng ký thành công'
        })
    return JsonResponse({
        'success': False,
        'message': 'Phương thức không được phép'
    })


@csrf_exempt
def updateItem(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        book_id = data.get('book_id')
        try:
            book = Book.objects.get(id=book_id, status='available')
            return JsonResponse({
                'message': 'Đã thêm vào giỏ hàng',
                'book': {
                    'id': book.id,
                    'title': book.title,
                    'price': float(book.price),
                    'imagePath': book.imagePath.url if book.imagePath else '/static/img/default_book.jpg',
                    'author': book.author or 'Không rõ',
                    'stock': book.stock,
                    'description': book.description or 'Chưa có mô tả'
                }
            })
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Sách không hợp lệ hoặc không có sẵn'}, status=400)
    return JsonResponse({'message': 'Phương thức không được phép'}, status=405)


def books(request):
    return home(request)


@csrf_exempt
def check_login_status(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({
                'success': True,
                'is_authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'full_name': request.user.full_name,
                    'phone': request.user.phone,
                    'address': request.user.address,
                    'status': request.user.status
                }
            })
        return JsonResponse({
            'success': True,
            'is_authenticated': False
        })
    return JsonResponse({'success': False, 'message': 'Phương thức không được phép'})

