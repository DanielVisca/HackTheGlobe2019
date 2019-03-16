from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse


# Create your views here.
def index(request):
	return HttpResponse("Hello World, you are at the Trade Platform index page.")

@csrf_exempt
def sms_response(request):
	#Start our TwiML response
	response = MessagingResponse()

	# Add a text message
	msg = response.message("Hello and welcome to TextTrade!")

	return HttpResponse(str(response))

