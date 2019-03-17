from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
# include decompose in your views.py
from django_twilio.request import decompose
from tradePlatform.models import User, Listing
# Do I need these next two?
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
	return HttpResponse("Hello World, you are at the Trade Platform index page.")

#Clear all variables
def clearAll():
	Trading=False
	Stage1=False
	Stage2=False
	Stage3=False

#Status variables
Trading=False
Stage1=False
Stage2=False
Stage3=False


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
	from_phone_number = twilio_request.from_
	#msg = response.message(str(from_phone_number))

	#ToDo: see if the phone number is in our database, 
	#	if it isnt, ask for their location
	#		when there is a response. Create a new User
	#		tell them how to use the app
	#	if it is, look at the text. Does it say 'Interested Listing_ID' or 'Trading'
	#		if 'trading' ask for them to say item, description etc... in specific format. Create Listing
	#			then calculate their distance to other users.
	#			if a user is within a certain distance, send them a message of the Listing and tell them to send back 'Interested Listing_ID'.
	#		if 'interested Listing_ID':
	#			respond with a message saying 'contact 'the number of the person who made the listing' to negotiate a trade and pickup'
	#			
	user = User.objects.filter(phoneNumber=from_phone_number) 
	#return HttpResponse(str(response))

	if user and Stage1==False:
		#text should look like "Interested in: 17" 
		text_body_split = twilio_request.body.split(':')

		if text_body_split[0].strip().lower()=="trading":
			Trading=True
			Stage1=True
			response.message("Please type the item you are trading followed by a ':' then the description of the item. ex: 'carrots: carrots picked 10 days ago'")
			return HttpResponse(response)

		elif text_body_split[0].strip().lower()=="interested in":
			Stage1=True
			listing_id = twilio_request.body.split(':')[1].strip()
			response.message("Your contact info has been sent to the owner of this listing")
			return HttpResponse(response)

		elif text_body_split[0].strip().lower()=="stop":
			clearAll()
			response.message("Thank you for using TMart. Please text to begin again")
			return HttpResponse(response)

		else:
			response.message("Please send a message in the form of 'Interested in: Listing number'. for example 'Interested in: 1'. Or 'Trading' Or type 'Stop'.")
			return HttpResponse(response)

	#elif user and Stage1==True and Stage2==False

	else:
		response.message("Welcome to TMart. What is you location? Please type your town or address (as if into google maps)")
		return HttpResponse(response)




	# Add a text message
	#msg = response.message(str(phone_number))