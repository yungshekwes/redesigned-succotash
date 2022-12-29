# UoH Cyber Security Project 1
## Link to Repository:

The repository is contained in Github: https://github.com/yungshekwes/redesigned-succotash

## Installation Instructions:

This project is built on Python 3 and therefore there is a requirement that in order to run the source code on one’s computer, it has to have Python 3 installed. Here is the link to install Python 3: https://www.python.org/downloads/ 

Additionally, the project contains some additional packages that need to be installed in order for the website to run properly. These can be downloaded with the following command:

```python
python3 -m pip install django requests
```

(This command will work under the assumption that pip is installed as it comes with Python 3, else, please do install pip as well)

## Testing Instructions:

First, make sure you run the following commands

```python
python3 manage.py migrate --run-syncdb
python3 manage.py runserver
```

Please make use of the following testing accounts, presented in (username, password) format:

- (Abhishek, Kumar)
- (Bill, Gates)
- (Steve, Jobs)

Additionally, if you would like to see the Django admin panel, go to http://localhost:8000/admin and log in with the following credential presented in (username, password) format:

- (administrator, admin1!)

If you would like wipe the database and testing with new accounts, please delete the db.sqlite3 file and then run the following commands:

```python
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py runserver
```

## FLAW 1 (CSRF):

**Exact links pinpointing the flaw:** 

1. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/views.py#L92
2. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/templates/helbank/transfer.html#L9

**Description of the flaw:** The flaw here is that the banking application makes use of a req.GET method without using any form of CSRF protection. This is evident clearly in the links above wherein the views.py file has the logic behind the transfer mechanism, and the transfer.html has the form for the request. Additionally, to prevent CSRF attacks, POST methods should be used, which is also highlighted in the links pinpointing the flaws.

To test the CSRF flaw out, there is a provided CSRF_Test.html file that can be used, located in the CSRF Vulnerability directory. This would transfer out 25 Euros from the first user account created to the third user account created. If the provided database is used, this would mean that the user “Abhishek” would lose 25 Euros and user “Bill” would suddenly be 25 Euros richer.

**How to fix it:** As suggested in the links to the flaws, the fix here would be to firstly add the CSRF verification token into transfer.html, and also change the GET methods in both the views.py and transfer.html to POST.

## FLAW 2 (A07:2021 – Identification and Authentication Failures): 

**Exact links pinpointing the flaw:**

1. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/views.py#L49

2. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/models.py#L5

**Description of the flaw:** As given by the OWASP description, the banking application “permits default, weak, or well-known passwords, such as ‘Password1’ or ‘admin/admin’”, as there are no minimum requirements for how the password should be formulated. Additionally, the passwords are stored in the database as plain text, which is an encryption problem that will be explained as part of the next flaw.

**How to fix it:** As given in the links to the flaws, the views.py file, specifically in the signup function, should contain a function that checks the user-supplied passwords against a list of common passwords, and/or ensure that there are some minimum requirements for the password, like being 12 alphanumeric characters at least, and having at least 2 symbols. 

## FLAW 3 (A02:2021 – Cryptographic Failures): 

**Exact links pinpointing the flaw:**

1. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/views.py#L40

2. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/models.py#L3

3. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/templates/helbank/manager.html#L22

**Description of the flaw:** The banking app does not encrypt passwords, account numbers, balances and other sensitive data of its users, instead storing it in the database as simply plaintext, and therefore, there is a high risk of sensitive data exposure. For example, without even being logged in, it is possible to guess the user who has managerial privileges and then access the manager screen and see everyone’s passwords. To test this, open up: http://localhost:8000/manager/1 and it is possible to see everyone’s passwords as well. 

**How to fix it:** The fix here would be to make use of the inbuilt Django User model from (django.contrib.auth.models), and like suggested in the sourcecode, make use of the capabilities for encryption of passwords for the users and then have an additional custom model that references the Django User model that contains the rest of the account information that does not necessarily need to be encrypted. Additionally, the password field on display in the manager page should also be removed.

## FLAW 4 (A03:2021 – Injection [SQL]): 

**Exact link pinpointing the flaw:** https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/views.py#L92

**Description of the flaw:** A raw SQL query is being used in the deposit function in views.py, which allows for malicious users to perform SQL injection attacks on the banking application website.

**How to fix it:** The fix here would be replacing the raw SQL query with Django Object Relational Mapper functions, as shown in the sourcecode given by the link. 

## FLAW 5 (A03:2021 – Injection [XSS]):

**Exact links pinpointing the flaws:**

1. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/views.py#L71

2. https://github.com/yungshekwes/redesigned-succotash/blob/main/helbank/templates/helbank/account.html#L13

**Description of the flaw:** Each user can enter their own account purpose, i.e.: savings, current, and so on. This was intended as a nifty function for users to better keep track of their money. However, the way it is implemented is makes the banking application vulnerable to cross-site scripting attacks. This is because the account.html file flags the users’ purposes to be safe. 

To simulate an XSS attack, log into the first user’s account, that is Abhishek’s account. Then go to the second user’s account, that is Steve’s account, by simply changing the ‘/account/1/’ to ‘/account/2/’. Once here, a new purpose can be created, like 

```html
<script>alert(“Your money is mine!”)</script>
```

 When Steve actually logs into their account, they would be greeted with an alert that says “Your money is mine!”.

**How to fix it:** To fix the XSS vulnerability, remove the safe tag from the owner.purpose that is given in the account.html file. Additionally, implement a function that checks if the Customer_id matches with that of the session, so that it is impossible to access someone else’ account while logged into an account.