from django.urls import path
from django.conf.urls import include
from employee import views


app_name = 'employee'

urlpatterns = [
    path('',views.employee_index,name='employee_index'),
    path('calender',views.calender,name='calender'),
    path('view/',views.emp_view_data,name='emp_view_data'),
    path('view/download',views.download_excel,name='download_excel'),



    

] 