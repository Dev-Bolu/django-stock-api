from datetime import date, timedelta
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ItemValue


# ------------------------------
# DAILY SALES SUMMARY
# ------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_sales_summary(request):
    today = date.today()
    totals = ItemValue.objects.filter(date_recorded=today).aggregate(
        total_sold=Sum('sold'),
        total_sales=Sum('total_price'),
        total_profit=Sum('profit'),
    )

    return Response({
        "date": str(today),
        "total_sold": totals['total_sold'] or 0,
        "total_sales": totals['total_sales'] or 0,
        "total_profit": totals['total_profit'] or 0,
    })


# ------------------------------
# WEEKLY SALES SUMMARY
# ------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_sales_summary(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday

    totals = ItemValue.objects.filter(date_recorded__range=[start_of_week, end_of_week]).aggregate(
        total_sold=Sum('sold'),
        total_sales=Sum('total_price'),
        total_profit=Sum('profit'),
    )

    return Response({
        "week_start": str(start_of_week),
        "week_end": str(end_of_week),
        "total_sold": totals['total_sold'] or 0,
        "total_sales": totals['total_sales'] or 0,
        "total_profit": totals['total_profit'] or 0,
    })


# ------------------------------
# MONTHLY SALES SUMMARY
# ------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_sales_summary(request):
    today = date.today()
    start_of_month = today.replace(day=1)

    totals = ItemValue.objects.filter(date_recorded__gte=start_of_month).aggregate(
        total_sold=Sum('sold'),
        total_sales=Sum('total_price'),
        total_profit=Sum('profit'),
    )

    return Response({
        "month": today.strftime("%B %Y"),
        "total_sold": totals['total_sold'] or 0,
        "total_sales": totals['total_sales'] or 0,
        "total_profit": totals['total_profit'] or 0,
    })
