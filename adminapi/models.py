from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.dispatch import receiver
from datetime import datetime, timedelta

# Create your models here.

class CustomUser(AbstractUser):
    user_type_choices=[
        ('Admin', 'Admin'),
        ('Bus Owner' ,'Bus Owner'),
        ('Passenger' ,'Passenger'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices)
    
    
class Admin(CustomUser):
    email_address=models.EmailField()                       
    
    
class BusOwner(CustomUser):
    phone=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=100)
    proof=models.ImageField(upload_to="images")
    # approval_choice=[
    #     ('Rejected', 'Rejected'),
    #     ('Pending' ,'Pending'),
    #     ('Approved' ,'Approved'),
    # ]
    # is_approved=models.CharField(max_length=50,choices=approval_choice,default="Pending")
    is_approved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

class BusDriver(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=100)
    license=models.ImageField(upload_to="image")
    age=models.IntegerField()
    dob=models.DateField()
    
    
class Passenger(CustomUser):
    phone=models.CharField(max_length=100,unique=True)
    email_address=models.EmailField(unique=True)
    address=models.CharField(max_length=100)


    def __str__(self):
        return self.username
    
    
    
class BusCategory(models.Model):
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.category 
    
    
class Bus(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images")
    Number_plate=models.CharField(max_length=500,unique=True)
    Engine_no=models.IntegerField(unique=True)
    RC_book=models.ImageField(upload_to="license")
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class Route(models.Model):
    name=models.CharField(max_length=200,unique=True)
    starts_from=models.CharField(max_length=200)
    ends_at=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Stop(models.Model):
    route=models.ForeignKey(Route,on_delete=models.CASCADE)
    stop_number=models.PositiveIntegerField()
    place=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images")
    link=models.CharField(max_length=100)
  
    def __str__(self):
        return self.place
    
    
class BusRoute(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    route=models.ForeignKey(Route,on_delete=models.CASCADE)
    buscategory=models.ForeignKey(BusCategory,on_delete=models.CASCADE)
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    amount=models.PositiveIntegerField()
    routetime=models.TimeField()

    def __str__(self):
        return self.route.name 
    
class BusRouteStops(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    busroute=models.ForeignKey(BusRoute,on_delete=models.CASCADE)
    stop=models.ForeignKey(Stop,on_delete=models.CASCADE)
    

class BusStopDetail(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE,null=True)
    busstop=models.OneToOneField(BusRouteStops,on_delete=models.CASCADE,unique=True)
    time=models.TimeField()
    amount=models.PositiveIntegerField()
   
  
