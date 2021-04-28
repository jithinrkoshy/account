from django.urls import path
from django.conf.urls import include
from home import views


app_name = 'home'

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home_page,name='home_page'),
    path('login',views.login_session,name='login_session'),
    path('logout',views.logout_session,name='logout_session'),
    path('accountadmin',views.admin,name='admin'),
    path('employee/',include('employee.urls',namespace='employee')),
    path('product/',include('product.urls',namespace='product'))


]