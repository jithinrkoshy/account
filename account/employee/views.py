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
import sys


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

@login_required
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

def cal_int_str(v_year,v_month,v_day):
    tmp_val = 0
    if(len(str(v_month)) == 1):
        v_month = "0" + str(v_month)
    else:
        v_month = str(v_month)
    if(len(str(v_day)) == 1):
        v_day = "0" + str(v_day)
    else:
        v_day = str(v_day) 
    date = str(v_year) + v_month + v_day    
    return date

def cal_int_str_dash(v_year,v_month,v_day):
    tmp_val = 0
    if(len(str(v_month)) == 1):
        v_month = "0" + str(v_month)
    else:
        v_month = str(v_month)
    if(len(str(v_day)) == 1):
        v_day = "0" + str(v_day)
    else:
        v_day = str(v_day) 
    date = str(v_year) +"-"+ v_month +"-"+ v_day    
    return date    
 

@login_required
def calender(request):

    if request.method == 'POST':
        date = request.POST['date']
      
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        days = get_days(year,month)
        start_day = dt(year,month,1).strftime("%a")
        log_flag = []
        inx=0
        for i in range(len(days)):
            log_flag.append(0)

        

        log_objs = LogDateFlag.objects.all()
        if(len(log_objs)!=0):
            for i in log_objs:
                tmp_dt = str(i.date)
                obj_day = int(tmp_dt.split("-")[2])
                obj_month = int(tmp_dt.split("-")[1])
                obj_year = int(tmp_dt.split("-")[0])
                if(obj_year==year and obj_month==month):
                    inx = days.index(obj_day)
                    log_flag[inx]=1

        l_day_list = len(days)
        today_date = str(dt.now()).split(" ")[0] 
        today_year =  today_date.split("-")[0]
        today_month =  today_date.split("-")[1]  
        today_day =  today_date.split("-")[2]
        today_date = today_year + today_month + today_day

        for i in range(l_day_list):
            passed_date = cal_int_str(year,month,days[i])
            
            if(passed_date>today_date):                          
                log_flag[i] = -1

        first_date = cal_int_str_dash(year,month,days[0])
        last_date = cal_int_str_dash(year,month,days[-1])   
        dl_objs = DailyLog.objects.filter(date__gte=first_date, date__lte=last_date)     
        for i in range(l_day_list):
            for j in dl_objs:
                if(cal_int_str_dash(year,month,days[i]) == str(j.date)):
                    if(j.work_status == 'na'):
                        log_flag[i] = 2


        return JsonResponse({'days':days,'log_flag':log_flag,'start_day':start_day})

    return JsonResponse({'days':"",'log_flag':"",'start_day':""})

def get_start_end(n,d_per_p,data_len):
    start_index = (n-1)*d_per_p
    end_index = n*d_per_p
    if(end_index>data_len):
        end_index = data_len
    return start_index,end_index  

@login_required
def emp_view_data(request):
    data = []
    flag=0
    if request.method == 'POST':
        
        first_date = request.POST['first_date']
        last_date  = request.POST['last_date'] 
        
        dla=None
        try:
            dla = DailyLogAdditional.objects.order_by('daily_log__date')
            
        except DailyLogAdditional.DoesNotExist:
            dla=None
        except:
            print(sys.exc_info()[0])    

        if(dla!=None):
            l = len(dla)
            x=0
            months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
            for i in range(l):
                flag=0
                tmp=[]
                if(str(dla[i].daily_log.date)>=first_date and str(dla[i].daily_log.date) <= last_date):
                    flag=1
                    x+=1
                tmp.append(str(x))
                tmp.append(str(dla[i].daily_log.employee.e_name))
                log_date = (str(dla[i].daily_log.date)).split("-")
                log_date = log_date[2] + "-" + months[log_date[1]] + "-" + log_date[0]
                tmp.append(str(log_date))
                
                tmp.append(str(dla[i].daily_log.work_status))
                tmp.append(str(dla[i].created_by))
                ct_dt = (str(dla[i].created_by_date)).split(".")[0]
                tmp.append(ct_dt)
                if(flag==1):
                    data.append(tmp)
        data_len = len(data)
        d_per_p = 10
        frag = math.ceil(data_len/d_per_p)
    
        n = int(request.POST['page_no'])
        start_index,end_index = get_start_end(n,d_per_p,data_len)
        final_data = data[start_index:end_index]    
        return JsonResponse({'final_data':final_data,'pages':frag})
    else:
        return render(request,'employee/empviewdata.html')


def get_excel(data):
    onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
    
    dy = dt.now()
    dy = dy.strftime("%d-%b-%Y")

    filename = ""
    filename = filename + "acc_"+dy + ".xlsx"
    x = 0
    while(filename in onlyfiles):
        x+=1
        filename_fhalf = filename.split(".")[0]
        filename = filename_fhalf + "_" + str(x) + ".xlsx"

        



    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('accsheet')

    cell_format_heading = workbook.add_format()
    cell_format_heading.set_border(1)
    cell_format_heading.set_bg_color('yellow')

    cell_format = workbook.add_format()  
    cell_format.set_border(1)

    cell_format_result = workbook.add_format()
    cell_format_result.set_border(1)
    cell_format_result.set_border_color('red')
    cell_format_result.set_align('center')
    cell_format_result.set_align('vcenter')

    row = 0
    col = 0
    header = ['Sid','Emp_name','Date','Work Status','(PM)Status(Vettu)','(PM)Status(Cheekal)','(PM)Status(Vettu&Cheekal)','(JN)Status(Vettu)','(JN)Status(Cheekal)','(JN)Status(Vettu&Cheekal)']
    tot_col = len(header)
    for i in range(tot_col):
        worksheet.write(row, col+i, header[i],cell_format_heading)
        

        
    row = 1
    col = 0

    
    tot_row = len(data)

    for i in range(tot_row):
        rec = data[i]
        for j in range(tot_col):
            item = rec[j]
            worksheet.write(row, col+j, item,cell_format)
        row+=1 
    worksheet.merge_range("A"+str(row+1)+":D"+str(row+1),'Total',cell_format)

    # for j in range(tot_col):
    # worksheet.write(row, 3, "=COUNTA(D2:D"+str(row)+")/2",cell_format)
    worksheet.write(row, 4, "=SUM(E2:E"+str(row)+")",cell_format)
    worksheet.write(row, 5, "=SUM(F2:F"+str(row)+")",cell_format)
    worksheet.write(row, 6, "=SUM(G2:G"+str(row)+")",cell_format)
    worksheet.write(row, 7, "=SUM(H2:H"+str(row)+")",cell_format)
    worksheet.write(row, 8, "=SUM(I2:I"+str(row)+")",cell_format)
    worksheet.write(row, 9, "=SUM(J2:J"+str(row)+")",cell_format)

    pm_f = "=SUM(E2:E"+str(row)+")"
    pm_h = "=SUM(F2:F"+str(row)+")"
    pm_fh = "=SUM(G2:G"+str(row)+")"
    jn_f = "=SUM(H2:H"+str(row)+")"
    jn_h = "=SUM(I2:I"+str(row)+")"
    jn_fh = "=SUM(J2:J"+str(row)+")"

    row+=1
    for i in range(tot_col):
        worksheet.write(row, col+i, "",cell_format)

    for i in range(5):
        row+=1
        for j in range(tot_col):
            if(i==0):
                worksheet.write(row, col+j, "",cell_format)
            elif(i==1):
                if(j==6):
                    worksheet.merge_range("E"+str(row+1)+":G"+str(row+1),'Podimon[v,c,vc]',cell_format)
                elif(j==9):
                    worksheet.merge_range("H"+str(row+1)+":J"+str(row+1),'John[v,c,vc]',cell_format)
                else:
                    worksheet.write(row, col+j, "",cell_format)
            elif(i==2):
                if(j==4):
                    worksheet.write(row, col+j, pm_f,cell_format)
                elif(j==5):
                    worksheet.write(row, col+j, pm_h,cell_format) 

                elif(j==6):
                    worksheet.write(row, col+j, pm_fh,cell_format) 

                elif(j==7):
                    worksheet.write(row, col+j, jn_f,cell_format)

                elif(j==8):
                    worksheet.write(row, col+j, jn_h,cell_format)

                elif(j==9):
                    worksheet.write(row, col+j, jn_fh,cell_format)           
                          
                else:                 
                    worksheet.write(row, col+j, "",cell_format)

            elif(i==3):
                worksheet.write(row, col+j, "",cell_format)  

            else:
                if(j==6):
                
                    worksheet.merge_range("E"+str(row)+":G"+str(row+1),'',cell_format_result)
                    worksheet.write(row-1, col+j-2, pm_f + "+" + pm_h[1:] + "+" + pm_fh[1:],cell_format_result)

                elif(j==9):
             
                    worksheet.merge_range("H"+str(row)+":J"+str(row+1),'',cell_format_result)               
                    worksheet.write(row-1, col+j-2, jn_f + "+" + jn_h[1:] + "+" + jn_fh[1:],cell_format_result)

                else:
                    worksheet.write(row, col+j, "",cell_format)                        



    workbook.close()
    return filename


@login_required
def download_excel(request , first_date = "2020-01-01",last_date = "2020-02-01"):
    
    data = []
    wk_full_int = {'f':1,'h':0,'fh':0,'na':0}
    wk_half_int = {'f':0,'h':1,'fh':0,'na':0}
    wk_full_half_int = {'f':0,'h':0,'fh':1,'na':0}
    try:
        tmp_obj = DailyLog.objects.filter(date__gte=first_date, date__lte=last_date).order_by('date')
    except DailyLog.DoesNotExist:
        tmp_obj = None
    if(tmp_obj != None):
        x=0
        for i in tmp_obj:
            x+=1
            tmp=[]
            tmp.append(x)
            tmp.append(i.employee.e_name)
            dt_log = str(i.date).split("-")
            dt_log = dt_log[2] + "-" + dt_log[1] + "-"  +  dt_log[0]
            tmp.append(dt_log)
            tmp.append(i.work_status)
            if(i.employee.e_id=='emp1'):

                tmp.append(wk_full_int[i.work_status])
                tmp.append(wk_half_int[i.work_status])
                tmp.append(wk_full_half_int[i.work_status])
                tmp.append(0)
                tmp.append(0)
                tmp.append(0)
            else:
                tmp.append(0)
                tmp.append(0)
                tmp.append(0)
                tmp.append(wk_full_int[i.work_status])
                tmp.append(wk_half_int[i.work_status])
                tmp.append(wk_full_half_int[i.work_status])

            


            data.append(tmp)
            

    path = get_excel(data)
 
    if os.path.exists(path):
            
        with open(path, "rb") as excel:
            data = excel.read()
        os.remove(path)
        response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=result_acc.xlsx'
        return response
    else:
        print('file does not exist')