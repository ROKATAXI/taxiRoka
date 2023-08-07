from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'payments/index.html')