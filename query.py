"""# Lấy tất cả sách
Book.objects.all()

# Lấy sách có id = 1
Book.objects.get(id=1)

# Lấy tất cả sách thuộc thể loại "Tiểu thuyết"
Category.objects.get(name="Tiểu thuyết").book_set.all()

# Lấy tất cả người dùng là "customer"
User.objects.filter(role="customer")

# Lấy tất cả đơn hàng của user có username là "customer1"
Order.objects.filter(user__username="customer1")

from django.db.models import Q

# Lấy sách có giá từ 100.000 đến 150.000
Book.objects.filter(price__gte=100000, price__lte=150000)

# Lấy sách có tiêu đề chứa từ "1984"
Book.objects.filter(title__icontains="1984")

# Lấy các đơn hàng không ở trạng thái "Completed"
Order.objects.exclude(status="Completed")

# Tìm sách có giá < 100k hoặc số lượng tồn kho > 20
Book.objects.filter(Q(price__lt=100000) | Q(stock__gt=20))

# Tạo mới một category
cat = Category.objects.create(name="Tâm lý học")

# Tạo mới một cuốn sách
Book.objects.create(title="Sách ABC", price=120000, category=cat, stock=10)

# Cập nhật giá sách có id = 1
book = Book.objects.get(id=1)
book.price = 135000
book.save()

# Cập nhật toàn bộ sách trong category "Khoa học" tăng giá thêm 10k
Book.objects.filter(category__name="Khoa học").update(price=models.F('price') + 10000)

# Xoá một sách
Book.objects.get(id=3).delete()

# Xoá tất cả đơn hàng ở trạng thái "Cancelled"
Order.objects.filter(status="Cancelled").delete()

# Lấy danh sách OrderDetail kèm thông tin sách
details = OrderDetail.objects.select_related('book').all()
for detail in details:
    print(detail.book.title, detail.quantity)

# Lấy danh sách OrderDetail của một đơn hàng cụ thể
order = Order.objects.get(id=1)
order.orderdetail_set.all()

from django.db.models import Count, Sum

# Tổng số sách đã bán ra (tính tổng quantity trong OrderDetail)
OrderDetail.objects.aggregate(total_quantity=Sum('quantity'))

# Đếm số lượng đơn hàng theo trạng thái
Order.objects.values('status').annotate(count=Count('id'))

# Đếm số sách trong từng thể loại
Book.objects.values('category__name').annotate(total=Count('id'))

# Sắp xếp sách theo giá tăng dần
Book.objects.order_by('price')

# Sắp xếp theo ngày tạo đơn hàng giảm dần
Order.objects.order_by('-created_at')

# Phân trang – lấy 5 sách đầu tiên
Book.objects.all()[:5]
"""