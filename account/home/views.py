from django.shortcuts import render
from home.forms import UserForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    authenticated = request.user.is_authenticated
    return render(request,'home/index.html',{'authenticated':authenticated})



def admin(request):
    registered = False
    admin_auth_key = "jrk898989#"
    error = False
    error_value = ""
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        inp_admin_ac = request.POST.get('id_admin_auth')
        inp_confirm_pass = request.POST.get('id_password_confirm')
        if(inp_admin_ac == admin_auth_key):
                       

            if(inp_confirm_pass == request.POST.get('password')):

                if user_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    registered = True
                else:
                    error=True
                    error_value = user_form.errors
                    print(error_value)
            else:
                error=True
                error_value = "Password are not matching"
                print(error_value)

        else:
            error=True
            error_value = "Invalid Auth Code"      
            print(error_value)
        return render(request,'home/admin.html',{'userform':user_form,'registered':registered,'error':error,'error_value':error_value})
    else:
        userform = UserForm()
        return render(request,'home/admin.html',{'userform':userform,'registered':registered,'error':error,'error_value':error_value})

def login_session(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home:home_page'))
            else: 
                print('Account not active') 
                return HttpResponseRedirect(reverse('home:index'))  
        else:
            error=True
            error_value = "Wrong Credentials"
            print('wrong Credentials') 
            print("Username: {} and password: {}".format(username,password)) 
            return render(request,'home/index.html',{'error':error,'error_value':error_value}) 
    else:
        return HttpResponseRedirect(reverse('home:index'))  

@login_required
def logout_session(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))

@login_required
def home_page(request):
    return render(request,'home/home.html')



# def employee_index(request):
#     return render(request,'employee/empindex.html')



