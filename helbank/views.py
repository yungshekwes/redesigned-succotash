from django.shortcuts import render, redirect
from .models import Customer
from django.urls import reverse
from django.db import connection
from random import sample
from string import digits

def index(req):
    if req.session.get("user_id", None):
        return redirect(reverse("account", kwargs = {"Customer_id" : req.session["user_id"]}))
    else:        
        return render(req, "helbank/index.html")

def error(req):
    return render(req, "helbank/error.html")

def login(req):
    if req.method == "GET":
        if req.session.get("user_id", None):
            return redirect(reverse("account", kwargs = {"Customer_id" : req.session["user_id"]}))
        else:        
            return render(req, "helbank/login.html")

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = Customer.objects.filter(username = username, password = password)
        if len(user) != 0:
            user_id = user[0].id
            req.session["user_id"] = user_id
            if user[0].status == 0:
                req.session["manager"] = True
            else:
                req.session["manager"] = False
            return redirect(reverse("account", kwargs = {"Customer_id" : user_id}))
        else:
            req.session["error"] = "Wrong username or password"
            return redirect("error")

# Flaw 3: No encryption of passwords used, and password is still stored in plaintext.
# Fix: Use the inbuilt Django User model which has capabilities for encryption of passwords for the users
# and have an additional custom model that references the Django User model. 
# Also remove the password field on display in the manager page.
def signup(req):
    if req.method == "GET":
        if req.session.get("user_id", None):
            return redirect(reverse("account", kwargs = {"Customer_id" : req.session["user_id"]}))
        else:        
            return render(req, "helbank/signup.html")
    
    if req.method == "POST":
        username = req.POST["username"]
        # Flaw 2: There is no checking mechanism for passwords to be more secure, i.e.: this allows '1234' to be a password.
        # Fix: Implementing a password checking function that ensures that a password is of a certain length,
        # contains alphanumeric characters and has some symbols, to make for a more secure password.
        password = req.POST["password"]
        if len(Customer.objects.filter(username = username)) != 0:
            req.session["error"] = "Username taken, try with another username!"
            return redirect("error") 
        else:
            randomAcc = "".join(sample(list(digits), 3)) + "-" + "".join(sample(list(digits), 3))+ "-" + "".join(sample(list(digits), 3))
            user = Customer.objects.create(username = username, password = password, balance = 100, account_number = randomAcc, status = 1) 
            user_id = user.id
            req.session["user_id"] = user_id
            if user.status == 0:
                req.session["manager"] = True
            else:
                req.session["manager"] = False
            return redirect(reverse("account", kwargs = {"Customer_id" : user_id}))            

def account(req, Customer_id):
    user = Customer.objects.get(id = Customer_id)

    if req.method == "POST":
        purpose = req.POST.get("purpose")
        user.purpose = purpose
        user.save()
        return redirect(reverse("account", kwargs = {"Customer_id" : Customer_id}))

    return render(req, "helbank/account.html", {"owner" : user})

def deposit(req, Customer_id):
    user = Customer.objects.get(id = Customer_id)
    req.session["message"] = ""
    if req.method == "GET":
        return render(req, "helbank/deposit.html", {"owner" : user})

    if req.method == "POST":
        amount = req.POST.get("amount")
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE helbank_Customer SET balance = balance + {amount} WHERE id = {Customer_id}")
                req.session["message"] = "Deposit Successful"
        except:
            req.session["message"] = "Deposit Failed" 

        return render(req, "helbank/deposit.html", {"owner" : user})     

def transfer(req, Customer_id):
    user = Customer.objects.get(id = Customer_id)
    users = Customer.objects.all()
    req.session["message"] = ""

    # Flaw 1: Using req.GET instead of req.POST
    # Fix: Change the req.GET... to req.POST
    if req.GET.get("to") != None and req.GET.get("amount") != None:
        recipient = Customer.objects.get(id = req.GET.get("to"))
        amount = int(req.GET.get("amount"))

        if amount <= 0:
            req.session["message"] = "Transfer Failed"      
        else:
            user.balance -= amount
            recipient.balance += amount
            user.save()
            recipient.save()
            req.session["message"] = "Transfer Successful"
    
    return render(req, "helbank/transfer.html", {"users" : users, "owner" : user})    
    
def manager(req, Customer_id):
    user = Customer.objects.get(id = Customer_id)
    users = Customer.objects.all()
    
    if req.method == "POST":
        if req.POST.get("new_manager_status") != None:
            manager = Customer.objects.get(id = req.POST.get("new_manager_status"))
            manager.status = 0
            manager.save()
        if req.POST.get("old_manager_status") != None:
            manager = Customer.objects.get(id = req.POST.get("old_manager_status"))
            manager.status = 1
            manager.save()
            
    return render(req, "helbank/manager.html", {"users" : users, "owner" : user})  

def logout(req):
    del req.session["user_id"]
    del req.session["manager"]

    return redirect("index")