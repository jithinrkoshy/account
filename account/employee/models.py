from django.db import models


# Create your models here.

class Employee(models.Model):
    e_id = models.CharField(max_length=20,unique=True)
    e_name = models.CharField(max_length=264)

    def __str__(self):
        return self.e_id

class DailyLog(models.Model):
  
    id=models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE) 
    date = models.DateField()
    emp_date_ckey = models.CharField(max_length=254,unique=True,default=id) 
    work_status = models.CharField(max_length=5,blank=True,null=True) 

   
    def __str__(self):
        return str(self.id)    


class DailyLogAdditional(models.Model):
    
    daily_log = models.ForeignKey('DailyLog',on_delete=models.CASCADE) 
    created_by = models.CharField(max_length=264)
    created_by_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=264)
    changed_by_date = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=264,blank=True)

    def __str__(self):
        return str(self.id)              

class LogDateFlag(models.Model):

    date = models.DateField(unique=True)
    log_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) 
