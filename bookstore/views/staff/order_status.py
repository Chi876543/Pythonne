# admin.py
from django.contrib import admin
from ...models import Order, OrderDetail

class OrderDetailInline(admin.TabularInline):  # hoặc StackedInline
    model = OrderDetail
    extra = 0  # Không hiển thị dòng trống thừa
    readonly_fields = ('book', 'quantity', 'price')  # nếu bạn muốn chỉ xem, không sửa

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    inlines = [OrderDetailInline]

