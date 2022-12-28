from django.db import models

class Customer(models.Model):
	username = models.TextField()
	password = models.TextField()
	balance = models.IntegerField()
	purpose = models.TextField(default = "")
	account_number = models.TextField(default = "123-456-789")
	status = models.IntegerField(default = 1) 
 	# Choose 1 for normal user else choose 0 for admin user