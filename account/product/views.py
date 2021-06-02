from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from product.models import ProductDailyLog,ProductDailyLogAdditional,ProductLogDateFlag
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


@login_required
def product_index(request):
    test=False

    if(request.user.username == 'test'):
        test=True

    print(test)    
    success=False
    error=False
    error_value = "Invalid Entries"
    year_list = get_years(2019)

    if request.method == 'POST':
        crt_flag = 0
        l_prod_cnt = request.POST.get('log-prod-count')
        l_prod_res_cnt = request.POST.get('log-prod-res-count')
     
        pdate = request.POST.get('log-prod-date')

        
       
        if(pdate!=None and pdate!=""):
            
            pdate = "-".join(pdate.split("/"))
        
            try:
                tmp_obj = ProductDailyLog.objects.get(date=pdate)
            except ProductDailyLog.DoesNotExist:
                tmp_obj = None
            if(tmp_obj == None):
                #checking for future dates
                today_date = str(dt.now()).split(" ")[0] 
                today_year =  today_date.split("-")[0]
                today_month =  today_date.split("-")[1]  
                today_day =  today_date.split("-")[2]
                today_date = today_year + "-" + today_month + "-" + today_day 

                #checking for future dates
                

                if(pdate > today_date):
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
            
            
            d_log_obj = ProductDailyLog(sheet_count=l_prod_cnt,sheet_residue_count=l_prod_res_cnt,date=pdate)
            d_log_obj.save()
            usr = request.user.first_name
            d_log_a_obj = ProductDailyLogAdditional(product_daily_log=d_log_obj,created_by=usr,changed_by=usr)
            d_log_a_obj.save()
            try:
                temp = ProductLogDateFlag.objects.get(date=pdate)
            except ProductLogDateFlag.DoesNotExist:
                temp=None
                
            if(temp==None):
                log_d_flag = ProductLogDateFlag(date=pdate,log_status=True)
                log_d_flag.save()
            success=True
            return render(request,'product/productindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list,'test':test})
        else:    
            return render(request,'product/productindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list,'test':test})

    return render(request,'product/productindex.html',{'success':success,'error':error,'error_value':error_value,'year_list':year_list,'test':test})



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

        

        log_objs = ProductLogDateFlag.objects.all()
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

        # first_date = cal_int_str_dash(year,month,days[0])
        # last_date = cal_int_str_dash(year,month,days[-1])   
        # dl_objs = DailyLog.objects.filter(date__gte=first_date, date__lte=last_date)     
        # for i in range(l_day_list):
        #     for j in dl_objs:
        #         if(cal_int_str_dash(year,month,days[i]) == str(j.date)):
        #             if(j.work_status == 'na'):
        #                 log_flag[i] = 2


        return JsonResponse({'days':days,'log_flag':log_flag,'start_day':start_day})

    return JsonResponse({'days':"",'log_flag':"",'start_day':""})


def get_start_end(n,d_per_p,data_len):
    start_index = (n-1)*d_per_p
    end_index = n*d_per_p
    if(end_index>data_len):
        end_index = data_len
    return start_index,end_index  


@login_required
def product_view_data(request):
    data = []
    count_sheets = 0
    # .filter(date__gte=first_date, date__lte=last_date)
    if request.method == 'POST': 
        first_date = request.POST['first_date']
        last_date  = request.POST['last_date'] 
        try:
            dla = ProductDailyLogAdditional.objects.filter(product_daily_log__date__gte=first_date, product_daily_log__date__lte=last_date).order_by('product_daily_log__date') 
        except ProductDailyLogAdditional.DoesNotExist:
            dla=None
        if(dla!=None):
            l = len(dla)
            months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
            for i in range(l):
                tmp=[]
                tmp.append(str(i+1))
                tmp.append(str(dla[i].product_daily_log.sheet_count))

                count_sheets = count_sheets + dla[i].product_daily_log.sheet_count

                tmp.append(str(dla[i].product_daily_log.sheet_residue_count))
                
                log_date = (str(dla[i].product_daily_log.date)).split("-")
                log_date = log_date[2] + "-" + months[log_date[1]] + "-" + log_date[0]
                tmp.append(str(log_date))
                
                tmp.append(str(dla[i].created_by))
                ct_dt = (str(dla[i].created_by_date)).split(".")[0]
                tmp.append(ct_dt)
                data.append(tmp)
              
        data_len = len(data)
        d_per_p = 10
        frag = math.ceil(data_len/d_per_p)
    
        n = int(request.POST['page_no'])
        start_index,end_index = get_start_end(n,d_per_p,data_len)
        final_data = data[start_index:end_index]    

        return JsonResponse({'final_data':final_data,'pages':frag,'count_sheets':count_sheets})
    else:
        return render(request,'product/productviewdata.html')    


 
def get_excel(data):
    onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
    
    dy = dt.now()
    dy = dy.strftime("%d-%b-%Y")

    filename = ""
    filename = filename + "product_acc_"+dy + ".xlsx"
    x = 0
    while(filename in onlyfiles):
        x+=1
        filename_fhalf = filename.split(".")[0]
        filename = filename_fhalf + "_" + str(x) + ".xlsx"

        

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('accsheet')


    cell_format = workbook.add_format()
    cell_format.set_border(1)

    row = 0
    col = 0
    header = ['SI_No','Date','Sheet Count','Sheet Residue Count']
    tot_col = len(header)
    for i in range(tot_col):
        worksheet.write(row, col+i, header[i],cell_format)
        

        
    row = 1
    col = 0

    tot_row = len(data)

    for i in range(tot_row):
        rec = data[i]
        for j in range(tot_col):
            item = rec[j]
            worksheet.write(row, col+j, item,cell_format)
        row+=1 
    worksheet.merge_range("A"+str(row+1)+":B"+str(row+1),'Total',cell_format)

    worksheet.write(row, 2, "=SUM(C2:C"+str(row)+")",cell_format)
    worksheet.write(row, 3, "=SUM(D2:D"+str(row)+")",cell_format)

    

    workbook.close()
    return filename

@login_required
def download_excel(request, first_date = "2020-01-01", last_date = "2020-02-01"):
    data = []

    try:
        tmp_obj = ProductDailyLog.objects.filter(date__gte=first_date, date__lte=last_date).order_by('date')
    except ProductDailyLog.DoesNotExist:
        tmp_obj = None
    if(tmp_obj != None):
        x=0
        for i in tmp_obj:
            x+=1
            tmp=[]
            tmp.append(x)
            
            dt_log = str(i.date).split("-")
            dt_log = dt_log[2] + "-" + dt_log[1] + "-"  +  dt_log[0]
            tmp.append(dt_log)
            tmp.append(i.sheet_count)
            tmp.append(i.sheet_residue_count)

            data.append(tmp)
            

    path = get_excel(data)
      
    if os.path.exists(path):
           
        with open(path, "rb") as excel:
            data = excel.read()
        os.remove(path)
        response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=product_result_acc.xlsx'
        return response
    else:
        print('file does not exist')       