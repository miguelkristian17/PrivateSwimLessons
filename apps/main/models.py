from django.db import models
import re, bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = ("Invalid email address!")
        if len(postData['firstName']) < 2:
            errors["fistName"] = "Fist name must be at least 2 characters!"
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last Name must be at least 2 characters!"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters!"
        if postData['password'] != postData['passwordConfirm']:
            errors["password"] = "Passwords do NOT match!"
        return errors
    def loginValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):          
            errors['loginEmail'] = ("Invalid email or password!")
        user = User.objects.filter(email = postData['email']) 
        if user:
            loggedUser = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), loggedUser.password.encode()):
                errors["password"] = "Invalid email or password!"
            return errors
        errors['loginEmail'] = ("Email not found!")
        return errors
    def editValidator(self, postData):
        errors = {}
        if len(postData['bio']) < 20:
            errors["bio"] = "Introduction must be at least 20 characters!"
        if len(postData['exp']) < 20:
            errors["exp"] = "Description must be at least 20 characters!"
        if int(postData['price']) > 100:
            errors["price"] = "Please input reasonable starting price!"
        if len(postData['specialty']) > 20:
            errors["specialty"] = "Specialty must be at most 20 characters!"
        if len(postData['location']) > 5:
            errors["location"] = "Location must be at most 5 characters!"
        return errors

class AppointmentManager(models.Manager):
    def appointmentValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = ("Invalid email address!")
        if len(postData['name']) < 3:
            errors["name"] = "Name must be at least 3 characters!"
        if len(postData['message']) < 20:
            errors["message"] = "Message must be at least 20 characters!"
        return errors

class ReviewManager(models.Manager):
    def reviewValidator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name must be at least 3 characters!"
        if len(postData['desc']) < 20:
            errors["desc"] = "Review must be at least 20 characters!"
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password= models.CharField(max_length = 255)
    bio = models.TextField(blank=True, null=True)
    exp = models.TextField(blank=True, null=True)
    timeExperience = models.TextField(blank=True, null=True)
    location = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    numAppointment = models.IntegerField(default = 0)
    rating = models.IntegerField(blank=True, null=True)
    specialty = models.TextField(blank=True, null=True)
    objects = UserManager()
    #instructorReview

class Appointment(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    poolAccess = models.CharField(max_length=50)
    availability = models.CharField(max_length=50)
    lesson = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    instructor = models.ForeignKey(User, related_name = "appointment", blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()


class Review(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    recommend = models.CharField(max_length=3,blank=True, null=True)
    bestFeature = models.CharField(max_length=30, blank=True, null=True)
    instructor = models.ForeignKey(User, related_name = "instructorReview", blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()