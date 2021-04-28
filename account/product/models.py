from django.db import models
from datetime import datetime as dt

# Create your models here.

d = str(dt.now()).split(" ")[0]


class ProductDailyLog(models.Model):
  
    id=models.AutoField(primary_key=True)
    sheet_count = models.IntegerField(default=0)
    sheet_residue_count = models.IntegerField(default=0) 
    date = models.DateField(unique=True) 

   
    def __str__(self):
        return str(self.id)    


class ProductDailyLogAdditional(models.Model):
    
    product_daily_log = models.ForeignKey('ProductDailyLog',on_delete=models.CASCADE) 
    created_by = models.CharField(max_length=264)
    created_by_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=264)
    changed_by_date = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=264,blank=True)

    def __str__(self):
        return str(self.id)              

class ProductLogDateFlag(models.Model):

    date = models.DateField(unique=True)
    log_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) 
