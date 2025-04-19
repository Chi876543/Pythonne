from django.contrib import admin
from .models import User, Book, Category, Order, StockIn, StockOut, Report_Inventory, Report_Revenue
from .views.admin.user_admin import UserAdmin
from .views.admin.book_admin import BookAdmin
from django.urls import path
from .views.manager.report_views import revenue_report_view, inventory_report_view
from .views.admin.category_admin import CategoryAdmin
from .views.staff.order_status import OrderAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(StockIn)
admin.site.register(StockOut)


class ReportAdmin1(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', revenue_report_view, name='admin_revenue_report'),
        ]
        return custom_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return revenue_report_view(request)

class ReportAdmin2(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', inventory_report_view, name='admin_inventoryreport'),
        ]
        return custom_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return inventory_report_view(request)

admin.site.register(Report_Revenue, ReportAdmin1)
admin.site.register(Report_Inventory, ReportAdmin2)
