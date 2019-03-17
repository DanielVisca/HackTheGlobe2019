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
from django.utils import timezone
from twilio.rest import Client

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

	if user:
		#text should look like "Interested in: 17" 
		text_body_split = twilio_request.body.split(':')


		if text_body_split[0].strip() != "Interested in" and text_body_split[0].strip() != 'Trading':
			# NoteToSelf: Does this send a message or does it need to return to send a message?
			
			# If the user wants to stop the text conversation
			# if twilio_request.body.strip() == 'stop':
			# 	response.message("Stopped")
			# 	return HttpResponse(response)
			response.message("Please send a message in the form of 'Interested in: Listing number'. for example 'Interested in: 1'. Or 'Trading: the item: the description' for example 'Trading: Moose : Willing to trade half a moose, shot 2 days ago''")
			return HttpResponse(response)
		
		# User has succesfully responded
		elif text_body_split[0].strip() == 'Interested in':
			listing_id = twilio_request.body.split(':')[1].strip()
			contactTrader(from_phone_number, listing_id)
			response.message("Your contact info has been sent to the owner of this listing")
			return HttpResponse(response)
			#text the owner of the listing
			# ToDo: how to text someone else. (use avkash's code)
			
		elif text_body_split[0].strip() == 'Trading':
			new_listing = Listing(user_id=user[0].id, item=text_body_split[1], description=text_body_split[2],date_added=timezone.now())
			new_listing.save()
			response.message("Your trade has been sent to locals, you will recieve a message from us when someone wants to Trade!")
			return HttpResponse(response)

	else:
		new_user = User(phoneNumber=from_phone_number, becameMember=timezone.now())
		new_user.save()
		response.message("You have been added to our trading platform. When you have something to Trade, text 'Trading: the item: the description' for example 'Trading: Moose : Willing to trade half a moose, shot 2 days ago'.\
			If you recieve a messaged about an item being traded in your area, text 'Interested in: listing_id' example 'Interested in: 3'.")
		return HttpResponse(response)



	# Add a text message
	#msg = response.message(str(phone_number))

	return HttpResponse(str(response))

def contactTrader(from_phone_number,listing_id):
	listing=Listing.objects.filter(id=listing_id)
	user_id=listing[0].user.id
	user=User.objects.filter(id=user_id)
	to_phone_number = user[0].phoneNumber
	account_sid = 'AC384a4f8fb39ec4a48f45cd8e40e4de2d'
	auth_token = 'c924cc19a0fbb9c9f26fbe3564ab0ebd'
	client = Client(account_sid, auth_token)
	message = client.messages \
	                .create(
	                     body="Good news! Someone is interested in the item ({}) you posted about. You can contact them at: {}".format(listing[0].item,from_phone_number),
	                     from_='+16042298878',
	                     to=to_phone_number
	                 )
	print(message.sid)

