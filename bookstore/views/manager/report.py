import calendar
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from ...models import Book, Order, StockIn, StockOut
from datetime import datetime
from django.utils import timezone
import json
from django.db.models.functions import TruncDay, TruncYear, TruncMonth


def home(request):
    return render(request, 'manager/report.html')

def revenue_by_month(start, end):
    if isinstance(start, str):
        start = timezone.make_aware(datetime.strptime(start, '%Y-%m-%d'))
    elif not timezone.is_aware(start):
        start = timezone.make_aware(start)

    if isinstance(end, str):
        end = timezone.make_aware(datetime.strptime(end, '%Y-%m-%d'))
        end = end.replace(day=calendar.monthrange(end.year, end.month)[1], hour=23, minute=59, second=59, microsecond=999999)
    elif not timezone.is_aware(end):
        end = timezone.make_aware(end)

    query_set = Order.objects.filter(status='Completed')
    query_set = query_set.filter(created_at__gte=start, created_at__lte=end)

    revenue_data = query_set.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_revenue=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('month')

    print(f"Revenue data: {list(revenue_data)}")
    return revenue_data

def revenue_by_day(start, end):
    if isinstance(start, str):
        start = timezone.make_aware(datetime.strptime(start, '%Y-%m-%d'))
    elif not timezone.is_aware(start):
        start = timezone.make_aware(start)

    if isinstance(end, str):
        end = timezone.make_aware(datetime.strptime(end, '%Y-%m-%d'))
    elif not timezone.is_aware(end):
        end = timezone.make_aware(end)

    end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
    query_set = Order.objects.filter(status='Completed')
    query_set = query_set.filter(created_at__gte=start, created_at__lte=end)

    revenue_data = query_set.annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total_revenue=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('day')

    return revenue_data

def revenue_by_year(start, end):
    if isinstance(start, str):
        start = timezone.make_aware(datetime.strptime(start, '%Y-%m-%d'))
    elif not timezone.is_aware(start):
        start = timezone.make_aware(start)

    if isinstance(end, str):
        end = timezone.make_aware(datetime.strptime(end, '%Y-%m-%d'))
    elif not timezone.is_aware(end):
        end = timezone.make_aware(end)

    end = end.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    query_set = Order.objects.filter(status='Completed')
    query_set = query_set.filter(created_at__gte=start, created_at__lte=end)

    revenue_data = query_set.annotate(
        year=TruncYear('created_at')
    ).values('year').annotate(
        total_revenue=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('year')

    print(f"Revenue data: {list(revenue_data)}")
    return revenue_data

@csrf_exempt
def revenue_api(request):
    """
    API trả về dữ liệu doanh thu cho Chart.js.
    Nhận: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "period": "day|month|year"}
    Trả về: {"labels": [], "revenues": [], "order_counts": []}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        start = data.get('start')
        end = data.get('end')
        period = data.get('period')

        if not all([start, end, period]):
            return JsonResponse({'error': 'Missing start, end, or period'}, status=400)

        if period not in ['day', 'month', 'year']:
            return JsonResponse({'error': 'Invalid period'}, status=400)

        if period == 'day':
            revenue_data = revenue_by_day(start, end)
        elif period == 'month':
            revenue_data = revenue_by_month(start, end)
        else:
            revenue_data = revenue_by_year(start, end)

        labels = []
        revenues = []
        order_counts = []

        for item in revenue_data:
            if period == 'day':
                label = item['day'].strftime('%Y-%m-%d')
            elif period == 'month':
                label = item['month'].strftime('%Y-%m')
            else:
                label = item['year'].strftime('%Y')

            labels.append(label)
            revenues.append(float(item['total_revenue']))
            order_counts.append(item['order_count'])

        return JsonResponse({
            'labels': labels,
            'revenues': revenues,
            'order_counts': order_counts
        })

    except ValueError as e:
        return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
def inventory_api(request):
    """
    API trả về dữ liệu tồn kho theo danh mục cho Chart.js.
    Nhận: Không cần tham số
    Trả về: {"labels": [danh mục], "stocks": [tổng tồn kho]}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        inventory_data = Book.objects.values('category__name').annotate(
            total_stock=Sum('stock')
        ).order_by('category__name')

        labels = [item['category__name'] or 'No Category' for item in inventory_data]
        stocks = [item['total_stock'] for item in inventory_data]

        return JsonResponse({
            'labels': labels,
            'stocks': stocks
        })

    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
