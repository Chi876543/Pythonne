from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.db.models import Sum, Count
from ...models import Order, OrderDetail, Book, StockIn
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from io import BytesIO
import datetime
from django.contrib.admin.views.decorators import staff_member_required

def chart_revenue_by_day(request):
    try:
        today = datetime.date.today()
        last_7_days = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]

        labels = []
        data = []

        for day in last_7_days:
            revenue = Order.objects.filter(
                created_at__date=day,
                status='Completed'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            labels.append(day.strftime('%d/%m'))
            data.append(revenue)

        plt.figure(figsize=(10, 5))
        plt.bar(labels, data, color='skyblue')
        plt.title('Doanh thu 7 ngày gần nhất')
        plt.xlabel('Ngày')
        plt.ylabel('Doanh thu (VND)')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return HttpResponse(buf.getvalue(), content_type='image/png')

    except Exception as e:
        print("LỖI KHI VẼ BIỂU ĐỒ REVENUE BY DAY:", e)
        return HttpResponse("Lỗi nội bộ server.", status=500)


# --- Biểu đồ doanh thu theo tháng ---
def chart_revenue_by_month(request):
    data = (Order.objects.filter(status='Completed')
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('total_amount'))
            .order_by('month'))

    labels = [d['month'].strftime('%m-%Y') for d in data]
    values = [d['total'] for d in data]

    return generate_chart(labels, values, 'Doanh thu theo tháng', 'Tháng', 'VNĐ')


# --- Biểu đồ doanh thu theo năm ---
def chart_revenue_by_year(request):
    data = (Order.objects.filter(status='Completed')
            .annotate(year=TruncYear('created_at'))
            .values('year')
            .annotate(total=Sum('total_amount'))
            .order_by('year'))

    labels = [str(d['year'].year) for d in data]
    values = [d['total'] for d in data]

    return generate_chart(labels, values, 'Doanh thu theo năm', 'Năm', 'VNĐ')


# --- Biểu đồ top 5 sản phẩm doanh thu cao nhất ---
def chart_top_5_revenue_products(request):
    data = (OrderDetail.objects
            .values('book__title')
            .annotate(total=Sum('price'))
            .order_by('-total')[:5])

    labels = [d['book__title'] for d in data]
    values = [d['total'] for d in data]

    return generate_chart(labels, values, 'Top 5 sách doanh thu cao nhất', 'Sách', 'VNĐ')


# --- Biểu đồ top 5 sản phẩm bán chạy ---
def chart_top_5_best_sellers(request):
    data = (OrderDetail.objects
            .values('book__title')
            .annotate(quantity=Sum('quantity'))
            .order_by('-quantity')[:5])

    labels = [d['book__title'] for d in data]
    values = [d['quantity'] for d in data]

    return generate_chart(labels, values, 'Top 5 sách bán chạy nhất', 'Sách', 'Số lượng')


# --- Biểu đồ top 5 sản phẩm bán chậm ---
def chart_top_5_worst_sellers(request):
    data = (OrderDetail.objects
            .values('book__title')
            .annotate(quantity=Sum('quantity'))
            .order_by('quantity')[:5])

    labels = [d['book__title'] for d in data]
    values = [d['quantity'] for d in data]

    return generate_chart(labels, values, 'Top 5 sách bán chậm nhất', 'Sách', 'Số lượng')


# --- Biểu đồ tồn kho hiện tại ---
def chart_inventory(request):
    data = Book.objects.all().values('title', 'stock').order_by('-stock')[:5]
    labels = [d['title'] for d in data]
    values = [d['stock'] for d in data]

    return generate_chart(labels, values, 'Top 5 sách tồn kho cao nhất', 'Sách', 'Số lượng tồn')


# --- Hàm tạo biểu đồ chung ---
def generate_chart(labels, values, title, xlabel, ylabel):
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')


# --- Giao diện báo cáo ---

def revenue_report_view(request):
    return render(request, 'manager/report/revenue_report.html')

def inventory_report_view(request):
    return render(request, 'manager/report/inventory_report.html')
