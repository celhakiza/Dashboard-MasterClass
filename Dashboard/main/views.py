from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    stats={
            'users':150,
            'Revenue': 200,
            'Errors':5
    }
    return render(request,'main/index.html',stats)

def intro(request):
    return HttpResponse("We are done!!")

