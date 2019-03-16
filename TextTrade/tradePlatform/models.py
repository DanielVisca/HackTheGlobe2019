from django.db import models

# Create your models here.
class User(models.Model):
	"""
	This creates a table that store all of the Users
	"""
	phoneNumber = models.IntegerField(default=5148896686)
	becameMember = models.DateTimeField('Date joined')
	location = models.CharField(max_length=200)

class Listing(models.Model):
	"""
	NoteToSelf: changed from 'Listings' to 'Listing', unmigrated.
	Add a new posting of an item that is on the market for trade
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	date_added = models.DateTimeField('Date posted')
