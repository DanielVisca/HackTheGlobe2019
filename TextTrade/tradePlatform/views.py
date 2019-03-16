from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return HttpResponse("Hello World, you are at the Trade Platform index page.")

def sms_response(request):
	return HttpResponse("SMS page.")

