from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from .models import User, Error, Session, Transaction
from datetime import timedelta
from django.http import HttpResponse
from .models import DashboardStat,Transaction,Error, User,Session
from django.db import connection
from types import SimpleNamespace
import requests
import json

#    stats = DashboardStat.objects.latest('created_at')
#    transactions = Transaction.objects.all().order_by('-created_at') #this sort data from the latest and list all rows from the trans
    
#   context = {
#    'users': stats.users,
#   'revenue': stats.revenue,
#    'errors': stats.errors,
#   'session': stats.session,
#   'transactions': transactions,
#   }
#   return render(request, 'main/index.html', context)

# Create your views here.
#def index(request):
#   stats={
#            'users':150,
 #           'Revenue': 400,
#            'Errors':5
 #   }
 #   return render(request,'main/index.html',stats)

# Get user count

def index(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) from main_user")
        user_count = cursor.fetchone()[0]

    #user_count = User.objects.count()
    
    # Calculate total revenue from all successful transactions
        cursor.execute("SELECT SUM(amount) from main_transaction where status = 'Paid'")
        total_revenue = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) from main_session where created_at::date = CURRENT_DATE")
        learned_sessions = cursor.fetchone()[0]
    
    # total_revenue = Transaction.objects.filter(status='Paid').aggregate(
    #     total=Sum('amount')
    # )['total'] or 0
    
    # For last 7 days stats:
    # date_filter = timezone.now() - timedelta(days=7)
    # today_errors = Error.objects.filter(
    #     created_at__gte=date_filter
    # ).count()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM main_error 
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
        """)
        today_errors = cursor.fetchone()[0]

    # Get active sessions count (example: sessions created today)
    # learned_sessions = Session.objects.filter(
    #     created_at__date=timezone.now().date()
    # ).count()
    
    # Get recent transactions

        cursor.execute("SELECT * FROM main_transaction ORDER BY created_at DESC LIMIT 5")
        rows = cursor.fetchall()
        recent_transactions =[
        SimpleNamespace(
        id=row[0],
        name=row[1],
        amount=row[2],
        status=row[3],
        created_at=row[4]
        )
        for row in rows
        ]
        #recent_transactions = Transaction.objects.order_by('created_at')[:10]

    context = {
        'users': user_count,
        'revenue': total_revenue,
        'errors': today_errors,
        'session': learned_sessions,
        'transactions': recent_transactions,
    }
    
    return render(request, 'main/index.html', context)

def intro(request):
    return HttpResponse("We are done!!")


def api(request):
  

    url = "https://iriseducationapp.com/api/get_student_details"

    payload = json.dumps({
    "student_code": "V1645"
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'PHPSESSID=a6989da398d0ab0b1bf077a48264107e'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # return HttpResponse(response.text)
    response = response.json()
    name = response.get("name")
    return HttpResponse(name)


def api_statistics(request):

    url = "https://vonsung.co.rw/trainingapi/getdata"

    payload = json.dumps({
    "format": "json",
    "limit":request.GET.get('limit','50')
    })
    headers = {
    'email': 'celestin.hakizimana@vonsung.co.rw',
    'phone': '+250785034947',
    'Content-Type': 'application/json',
    'Cookie': 'ci_session=a7de08c3b3a584ce22bc8d127e4e2a4b4a88a2e9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Get data from json response (first check from your Postman how the data looks like)
    data = response.json()
    products = data.get("products", [])
    categories = list(set(p['category'] for p in products))
    total_products = len(products)
    total_stock = sum(int(p['stock_quantity']) for p in products)
    avg_price = round(sum(float(p['price']) for p in products)/total_products)
 # Top 10 by stock
    top_products = sorted(products, key=lambda x: int(x['stock_quantity']),
    reverse=False)[:10]
    context = {
    "user": data.get("user"),
    "email": data.get("email"),
    "total_products": total_products,
    "distinct_categories": len(categories),
    "total_stock": total_stock,
    "average_price": avg_price,
    "top_products": top_products,
    }
    return render(request, "main/products_dashboard.html", context)

