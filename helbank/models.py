from django.db import models

class Customer(models.Model):
	username = models.TextField()
	# Flaw 2: There is no checking mechanism for passwords to be more secure, i.e.: this allows '1234' to be a password.
    # Fix: Implementing a password checking function that ensures that a password is of a certain length,
    # contains alphanumeric characters and has some symbols, to make for a more secure password.
	password = models.TextField()
	balance = models.IntegerField()
	purpose = models.TextField(default = "")
	account_number = models.TextField(default = "123-456-789")
	status = models.IntegerField(default = 1) 
 	# Choose 1 for normal user else choose 0 for admin user