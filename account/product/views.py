from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from employee.models import Employee,DailyLog,DailyLogAdditional,LogDateFlag
from django.http import HttpResponseRedirect,HttpResponse
import xlsxwriter
from datetime import datetime as dt
import math
import os
from os import listdir
from os.path import isfile, join



# Create your views here.
def get_days(year,month):
    
    tmp=[]
    try:
        for i in range(1,40):
            tmp.append(dt(year,month,i).day)
    except ValueError:
        pass		
    
   
    return tmp
def get_years(start_year): 
    
    cur_year = dt.now().year
    year_list = []
    x=start_year

    while(x<=cur_year):
        year_list.append(x)
        x+=1
    return year_list 

def employee_index(request):
    success=False
    error=False
    error_value = "Invalid Entries"
    year_list = get_years(2019)

    if request.method == 'POST':
        crt_flag = 0
        ename = request.POST.get('log-emp-name')
        e_obj = Employee.objects.get(e_name=ename)
        edate = request.POST.get('log-emp-date')
        
        ework = request.POST.get('log-emp-work')
        
       
        if(e_obj!=None and edate!=None and edate!=""):
            
            edate = "-".join(edate.split("/"))
            emp_dt_ckey = ename + "-" + edate
            try:
                tmp_obj = DailyLog.objects.get(emp_date_ckey=emp_dt_ckey)
            except DailyLog.DoesNotExist:
                tmp_obj = None
            if(tmp_obj == None):
                #checking for future dates
                today_date = str(dt.now()).split(" ")[0] 
                today_year =  today_date.split("-")[0]
                today_month =  today_date.split("-")[1]  
                today_day =  today_date.split("-")[2]
                today_date = today_year + "-" + today_month + "-" + today_day 

                #checking for future dates
                

                if(edate > today_date):
                    error=True
                    error_value = "Future Date"
                else:
                    crt_flag=1  
                
            else:      
                error=True
                error_value = "Data already exists"     
        else:
            error=True

        if crt_flag==1:
            
            
            d_log_obj = DailyLog(employee=e_obj,date=edate,emp_date_ckey=emp_dt_ckey,work_status=ework)
            d_log_obj.save()
            usr = request.user.first_name
            d_log_a_obj = DailyLogAdditional(daily_log=d_log_obj,created_by=usr,changed_by=usr)
            d_log_a_obj.save()
            try:
                temp = LogDateFlag.objects.get(date=edate)
            except LogDateFlag.DoesNotExist:
                temp=None
                
            if(temp==None):
                log_d_flag = LogDateFlag(date=edate,log_status=True)
                log_d_flag.save()
            success=True
            return render(request,'employee/empindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list})
        else:    
            return render(request,'employee/empindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list})

    return render(request,'employee/empindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list})

