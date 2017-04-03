from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def basic_test(request):
    return JsonResponse({'id': 2}, content_type="application_type")