from django.shortcuts import render

# Create your views here.
def matching_list(request):
    return render(request, 'matching/matchinglist.html')