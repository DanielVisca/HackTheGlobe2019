from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
# include decompose in your views.py
from django_twilio.request import decompose

# Create your views here.
def index(request):
	return HttpResponse("Hello World, you are at the Trade Platform index page.")

@csrf_exempt
def sms_response(request):
	"""
	This is a webhook that recieves text messages.
	ToDo: new phone numbers are added to database

	"""
	# from_number = request.form['From']
	# body = request.form['To']
	#Start our TwiML response
	response = MessagingResponse()

	twilio_request = decompose(request)
	phone_number = twilio_request.to
	# Add a text message
	msg = response.message(str(phone_number))

	return HttpResponse(str(response))

