import json
from django.http import JsonResponse
from django.shortcuts import render
from ...models import Book, Order, OrderDetail, User
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

def profile(request):
    return render(request ,'customer/profile.html')

def cart(request):
    return render(request, 'customer/cart.html')

def get_book(request):
    if request.method == 'GET':
        books = Book.objects.filter(status='available')
        books_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock': book.stock,
            'imagePath': book.imagePath.url if book.imagePath else None,
        }
        for book in books
        ]
    return JsonResponse(books_data, safe=False)


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
    
            user_id = data.get('user_id')
            address = data.get('address')
            cart = data.get('cart', [])

            if not user_id or not address or not cart:
                return JsonResponse({'error': 'Thiếu thông tin đơn hàng'}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Người dùng không tồn tại'}, status=404)

            total = 0
            for item in cart:
                total += float(item.get('price'))

            # Tạo Order
            order = Order.objects.create(
                user=user,
                address=address,
                total_amount=total,
                status='Pending'  
            )


            # Tạo các OrderDetail
            for item in cart:
                book_id = item.get('book_id')
                quantity = int(item.get('quantity'))
                unit_price = float(item.get('price'))

                try:
                    book = Book.objects.get(id=book_id)
                except Book.DoesNotExist:
                    return JsonResponse({'error': 'Không thấy sách'}, status=404)

                OrderDetail.objects.create(
                    order=order,
                    book=book,
                    quantity=quantity,
                    price=unit_price  
                )

            return JsonResponse({'message': 'Tạo đơn hàng thành công', 'order_id': order.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=405)
        
@csrf_exempt
def view_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')

            if not user_id:
                return JsonResponse({'error': 'Missing user_id'}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            orders = Order.objects.filter(user=user).order_by('-created_at')

            result = []
            for order in orders:
                order_details = OrderDetail.objects.filter(order=order).select_related('book')
                items = []
                for detail in order_details:
                    items.append({
                        'book_title': detail.book.title,
                        'quantity': detail.quantity,
                        'price': detail.price,
                        'total': detail.quantity * detail.price
                    })

                result.append({
                    'order_id': order.id,
                    'address' : order.address,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': order.status,
                    'total_amount': sum(item['total'] for item in items),
                    'items': items
                })

            return JsonResponse(result, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def search_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            start_date = data.get('startDate')
            end_date = data.get('endDate')
            total = data.get('total')
            address = data.get('address', '').strip()
            status = data.get('status', '').strip()

            orders = Order.objects.all().order_by('-created_at')

            if user_id:
                orders = orders.filter(user_id=user_id)

            if start_date:
                orders = orders.filter(created_at__date__gte=start_date)

            if end_date:
                orders = orders.filter(created_at__date__lte=end_date)

            if address:
                orders = orders.filter(address__icontains=address)

            if status:
                orders = orders.filter(status__icontains=status)

            # Lọc theo khoảng total (20%)
            if total and str(total).strip().isdigit():
                total_value = float(total)
                lower = total_value * 0.8
                upper = total_value * 1.2
                orders = [order for order in orders if lower <= order.get_total() <= upper]

            result = []
            for order in orders:
                order_details = OrderDetail.objects.filter(order=order).select_related('book')
                items = [{
                    'book_title': detail.book.title,
                    'quantity': detail.quantity,
                    'price': detail.price,
                    'total': detail.quantity * detail.price
                } for detail in order_details]

                result.append({
                    'order_id': order.id,
                    'address': order.address,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': order.status,
                    'total_amount': sum(item['total'] for item in items),
                    'items': items
                })

            return JsonResponse(result, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
