from django.db import models

# Create your models here.

class Customer(models.Model):
    customer=models.IntegerField(primary_key=True, default=0)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    gender=models.CharField(max_length=1)
    age=models.IntegerField()
    address=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    

class Account(models.Model):
    customer=models.ForeignKey('Customer',default=0,on_delete=models.CASCADE)
    saving_acc=models.CharField(max_length=50,null=True,blank=True)
    fixed_acc=models.CharField(max_length=50,null=True,blank=True)
    s_balance=models.BigIntegerField(default=0)
    f_balance=models.BigIntegerField(default=0)

class Admin(models.Model):
    name=models.CharField(max_length=30,default='')
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=20)

class Contact(models.Model):
    query_no=models.IntegerField(primary_key=True, default=0)
    customer_id=models.IntegerField()
    customer_name=models.CharField(max_length=30)
    query_data=models.CharField(max_length=100)

    