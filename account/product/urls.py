from django.urls import path
from django.conf.urls import include
from product import views


app_name = 'product'

urlpatterns = [
    path('',views.product_index,name='product_index'),
    path('calender',views.calender,name='calender'),
    path('view/',views.product_view_data,name='product_view_data'),
    path('view/download',views.download_excel,name='download_excel'),
  
 


    

] 