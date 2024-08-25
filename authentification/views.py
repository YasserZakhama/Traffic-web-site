from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from myproject import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return(render(request,'authentification/index.html'))

def signup(request):
    if request.method =="POST":

        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist ! Please try an other one. ')
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, 'This email already registred !')
            return redirect('signup')

        if pass2 !=pass1 :
            messages.error(request, 'Password didnt match ! ')
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, 'Username too long ! It must be under 10 caracters ')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,'Your Account has been successfully created. We have also send you a confermation email, please confirm your email addres to order to actovate your account.')

        ''''
        #Welcome Email
        subject = "welcome to traffic web site - Django Login!!"
        message = "Hello "+ myuser.first_name +"!! \n" + " Welcome to Traffic web site \n Thank you dor visiting our website \n We have also send you a confermation email, please confirm your email addres to order to actovate your account. \n\n Thanking You\n Yasser Zakhama"
        from_email = settings.EMAIL_HOST_USER
        to_liste = [myuser.email]

        try:
            send_mail(subject, message, from_email, to_liste, fail_silently=False)
            print("Email sent successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        '''
        
        return redirect('signin')

    return(render(request,'authentification/signup.html'))

def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        user = authenticate(username=username , password =pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return redirect('packet_list')
        else:
            messages.error(request,'Username or Password is Incorect !!')
            return redirect('signin')
    return(render(request,'authentification/signin.html'))

def signout(request):
    logout(request)
    messages.success(request,'You logged out successfully ')
    return redirect('home')
