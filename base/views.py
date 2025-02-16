# from imaplib import _Authenticator
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from base.models import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import random
from . mail import mail
import csv

# Create your views here.
def home(request):
    # return redirect('/merch')
    context = {}
    event_dates = EventDates.objects.filter(type="home").order_by('-event_start').first()
    # print(event_dates)
    msg = "Esummit has ended"
    time_diff = -1
    end = True
    if event_dates is not None:
        current_time = timezone.now()
        time_diff = 0
        end = False
        if event_dates.event_start > current_time:
            # hunt is yet to begin
            time_diff = (event_dates.event_start - current_time).total_seconds()
            msg = "E-summit Starts in"
        elif event_dates.event_end > current_time:
            time_diff = (event_dates.event_end - current_time).total_seconds()
            msg = "E-summit Ends in"
        else:
            time_diff = (event_dates.event_end - current_time).total_seconds()
            msg = "E-summit has ended"
            end = True
    context['msg'] = msg
    context['time_diff'] = int(time_diff)
    context['has_ended'] = end
    return render(request,'home.html',context)

def handleLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('/')

        user = User.objects.filter(email=email).first()
        user = authenticate(request, username=user.username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('/')

        return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def handleSignUp(request):
    if request.method == 'POST':
        request.session['username'] = request.POST.get('username')
        request.session['email'] = request.POST.get('email')
        request.session['password'] = request.POST.get('password')
        # if 'get_otp' in request.POST:
        generated_otp = random.randint(1000, 9999)
        # print(generated_otp)
        request.session['generated_otp'] = generated_otp
        mail(request.POST.get('email'), generated_otp)
        return redirect('/verify')
    else:
        return render(request, 'register.html')

def verify(request):
    if request.method == 'POST':
        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        user_entered_otp = request.POST.get('otp')
        if user_entered_otp == str(request.session.get('generated_otp')):
            # user = User.(username=username, email=email, password=password)
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('/login')
        else:
            return render(request, 'verify.html', {'otp_failed': True})
    else:
        return render(request, 'verify.html')

# @login_required
def merch(request):
    # if request.user.is_authenticated == False:
    #     return redirect("/accounts/google/login/?next=/merch")
    if request.method == 'POST':
        # Create a new Merches instance and save it to the database        
        merch = Merch.objects.create(
            user=request.user,
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone_number = request.POST.get('phone_number'),
            from_college = request.POST.get('from_college'),
            reg_no = request.POST.get('reg'),
            roll_no = request.POST.get('roll'),
            hall_no = request.POST.get('hall'),
            room_no = request.POST.get('room'),
            address = request.POST.get('address'),
            size = request.POST.get('size'),
            payment= request.POST.get('payment'),
            verified=False
        )
        merch.save()
        # print(request.POST['image'])
        proof =Proof.objects.create(user=request.user, image=request.FILES.get('image'))
        
        # print(request.FILES['image'])
        proof.save()
        return redirect('/success')

    # Render the form template for GET requests
    return render(request, 'merch.html')

def successPage(request):
    return render(request, 'success.html')


def passes(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        proof_image = request.FILES.get('image')

        if not proof_image:
            return HttpResponse("No image uploaded", status=400)

        new_pass = Pass.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            plan=plan, 
            verified=False,
            image=proof_image
        )

        return render(request, 'success.html')

    return render(request, 'pass.html')




def comingsoonPage(request):
    return render(request, "comingsoon.html")

def qr(request):
    return render(request, "qr/home.html")

# @login_required
def data(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="merch.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Mobile', 'Email', 'Size', 'Payment'])

        merch_items = Merch.objects.all().values_list('name', 'phone_number', 'email', 'size', 'payment')
        for merch_item in merch_items:
            writer.writerow(merch_item)

        return response
    else:
       return redirect('/')