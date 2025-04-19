# bookstore/urls.py
from django.urls import path

from bookstore.views.manager import report_views
from .views.customer import home
from .views.customer import profile
from .views.admin import admin
from .views.staff import order_status
from .views.staff import stock_in
from .views.staff import stock_out
from .views.admin import book_admin
from .views.admin import user_admin
from .views.admin import group_permission

urlpatterns = [
    path('', home.home, name='home'),
    path('books/', home.books, name='books'),
    path('profile/', profile.profile, name = 'profile'),
    path('cart/', profile.cart, name = 'cart'),

    path('admin/', admin.admin_login, name = 'admin_login'),
    path('admin/login/', admin.admin_login_view, name = 'admin_login_view'),
    path('admin/logout/', admin.admin_logout, name = 'admin_logout'),

    # Quản lý Group Permission
    path('admin/list_group', group_permission.admin_list_group, name = 'list_group'),

    # Quản lý người dùng
    path('admin/list_user', user_admin.admin_list_users, name = 'list_user'),
    
    # Quản lý sách
    path('admin/list_book', book_admin.admin_list_books, name = 'list_book'),

    # Quản lý danh mục
    #path('admin/list_category', category_admin.admin_list_category, name = 'list_category'),

    # Quản lý đơn hàng
    path('admin/list_order',order_status. admin_list_orders, name = 'list_order'),

    # Quản lý phiếu nhập
    path('admin/list_stockin',stock_in.admin_stock_in, name = 'list_stock_in'),

    # Quản lý phiếu xuất
    path('admin/list_stockout', stock_out.admin_stock_out, name = 'list_stock_out'),



    path('api/create_order/', profile.create_order, name = 'create-order'),
    path('api/view_order/', profile.view_order, name= 'view-order'),
    path('api/search_order/', profile.search_order, name= 'search-order'),
    path('api/get_book/', profile.get_book, name = 'get-books'),

    path('manager/report/revenue/', report_views.revenue_report_view, name='revenue_report'),
    path('manager/report/inventory/', report_views.inventory_report_view, name='inventory_report'),

    # Biểu đồ
    path('chart/revenue/day/', report_views.chart_revenue_by_day, name='chart_revenue_day'),
    path('chart/revenue/month/', report_views.chart_revenue_by_month, name='chart_revenue_month'),
    path('chart/revenue/year/', report_views.chart_revenue_by_year, name='chart_revenue_year'),
    path('chart/revenue/top/', report_views.chart_top_5_revenue_products, name='chart_top_revenue'),
    path('chart/sales/best/', report_views.chart_top_5_best_sellers, name='chart_best_seller'),
    path('chart/sales/worst/', report_views.chart_top_5_worst_sellers, name='chart_worst_seller'),
    path('chart/inventory/', report_views.chart_inventory, name='chart_inventory'),

]