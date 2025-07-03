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
    user_count = User.objects.count()
    
    # Calculate total revenue from all successful transactions
    total_revenue = Transaction.objects.filter(status='Paid').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # For last 7 days stats:
    date_filter = timezone.now() - timedelta(days=7)
    today_errors = Error.objects.filter(
        created_at__gte=date_filter
    ).count()
    # Get active sessions count (example: sessions created today)
    learned_sessions = Session.objects.filter(
        created_at__date=timezone.now().date()
    ).count()
    
    # Get recent transactions
    recent_transactions = Transaction.objects.order_by('created_at')[:10]

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

