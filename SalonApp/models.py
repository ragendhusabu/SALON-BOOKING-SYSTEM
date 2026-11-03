from django.db import models

# Create your models here.
class StaffDb(models.Model):
    staff_name  =models.CharField(max_length=100)
    specialization =models.CharField(max_length=100)
    experience =models.IntegerField() 
    phone = models.CharField (max_length=15)

class AppoinmentDb(models.Model):
   
    staff =models.ForeignKey ( StaffDb ,on_delete=models.CASCADE)
    customer_name =models.CharField(max_length=100) 
    service_name = models.CharField(max_length=100)  
    appointment_date = models.DateField() 
    appointment_time =  models.TimeField(editable=False, null=True) 
    amount =models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=200, default="pending..")