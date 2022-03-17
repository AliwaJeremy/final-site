import numbers
from socket import IP_DROP_MEMBERSHIP
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, FileResponse
import africastalking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout as logouts, authenticate, login as logsin
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ackweb.decorators import unauthenticated_user, allowed_users, superuser_only
from django.contrib.auth.models import Group
from ackweb.models import *
from ackweb.filters import AccountFilter 
from .forms import *
from .resources import AttendanceResource
from tablib import Dataset
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django_email_verification import send_email as sendConfirm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
import random
import string
from django.template.loader import get_template
from django.template import Context



def download_file(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf , pagesize = letter, bottomup = 0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    accounts = Account.objects.all()
    lines = []
    for account in accounts:
        lines.append(account.first_name)
        lines.append(account.last_name)
        lines.append(account.email)
        lines.append(account.membership_number)
        lines.append(account.mobile_number)
        lines.append( '')
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Accounts.pdf')

@login_required(login_url='login')
def forms(request):
    return render (request, "forms.html")

@login_required(login_url='login')
@superuser_only
def send_sms(request):
    username = settings.AT_USER_NAME   
    api_key = settings.AT_API_KEY      
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    if request.method == "POST":
       recepients = [request.POST.get('recepient')]
       message = request.POST.get('message')
       response = sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)
       messages.success(request, f'message sent succsesfully')
       render(request, "send_smss.html", {"response":response})
       return redirect ('send_smss')
    return render(request, "send_sms.html")

@login_required(login_url='login')
@superuser_only
def all_sms(request):
    username = settings.AT_USER_NAME   
    api_key = settings.AT_API_KEY      
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    if request.method == "POST":
       message = request.POST.get('message')
       reciever = Account.objects.all()
       dependent_reciever = Dependent.objects.all()
       recepient = list(i for i in reciever.values_list('mobile_number', flat=True) if bool(i))
       dependent_recepient = list(i for i in dependent_reciever.values_list('mobile_number', flat=True) if bool(i))
       recepients = recepient + dependent_recepient
       response = sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)
       messages.success(request, f'message sent succsesfully')
       render(request, "send_smss.html", {"response":response})
       return redirect ('send_smss')
    return render(request, "all_sms.html")

@login_required(login_url='login')
def offering(request):
    username = settings.AT_USER_NAME   
    api_key = settings.AT_API_KEY      
    africastalking.initialize(username, api_key)
    payment = africastalking.Payment
    productName = "STKPUSH"
    phoneNumber = request.user.mobile_number
    currencyCode = "KES"
    if request.method == "POST":
       amount = request.POST.get('amount')
       metadata = {"agentId" : "654", "productId" : "321"}
       provider_channel = '1122'
       try:
           result = payment.mobile_checkout(productName, phoneNumber, currencyCode, amount, metadata)#provider_channel)
           return redirect('userhome')
       except Exception as e:
           print ("Received error response:%s" %str(e))
    return render(request, "offering.html")

@login_required(login_url='login')
@superuser_only
def department_sms(request):
    department = Department.objects.all()
    ministry = Ministry.objects.all()
    cluster = Cluster.objects.all()
    if request.method == 'POST':
       username = settings.AT_USER_NAME   
       api_key = settings.AT_API_KEY      
       africastalking.initialize(username, api_key)
       sms = africastalking.SMS
       dept = request.POST.get('department_name')
       try:
           group = Department.objects.get(name = dept)
       except Department.DoesNotExist:
           group = None
       try:
           group1 = Cluster.objects.get(name = dept)
       except Cluster.DoesNotExist:
           group1 = None
       try:
           group2 = Ministry.objects.get(name = dept)
       except Ministry.DoesNotExist:
           group2 = None
       reciever1 = Account.objects.filter(department = group)
       dependent_reciever1 = Dependent.objects.filter(department = group)
       reciever2 = Account.objects.filter(cluster = group1)
       dependent_reciever2 = Dependent.objects.filter(cluster = group1)
       reciever3 = Account.objects.filter(ministry = group2)
       dependent_reciever3 = Dependent.objects.filter(ministry = group2)
       recepient1 = list(i for i in reciever1.values_list('mobile_number', flat=True) if bool(i))
       dependent_recepient1 = list(i for i in dependent_reciever1.values_list('mobile_number', flat=True) if bool(i))
       recepient2 = list(i for i in reciever2.values_list('mobile_number', flat=True) if bool(i))
       dependent_recepient2 = list(i for i in dependent_reciever2.values_list('mobile_number', flat=True) if bool(i))
       recepient3 = list(i for i in reciever3.values_list('mobile_number', flat=True) if bool(i))
       dependent_recepient3 = list(i for i in dependent_reciever3.values_list('mobile_number', flat=True) if bool(i))
       recepients = recepient1 + dependent_recepient1 + recepient2 + dependent_recepient2 + recepient3 + dependent_recepient3
       message = request.POST.get('message')
       sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)
       messages.success(request, f'message sent succsesfully')
       return redirect('superuser_home')
    else:
       context = {"department":department, "cluster":cluster, "ministry":ministry}
       return render(request, "department_sms.html", context)

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def church_reg(request):
    return render(request, 'church_reg.html')

def clusters(request):
    return render(request, 'clusters.html')

def contact(request):
     if request.method == 'POST':
        subject =request.POST.get('name')
        message = request.POST.get('message')
        sendfrom = request.POST.get('email')
        reciever = settings.EMAIL_HOST_USER
        send_mail(subject, message, sendfrom, [reciever])
        return redirect('index')
     return render(request, 'contact.html')

def departments(request):
    return render(request, 'departments.html')

def kama(request):
    return render(request, 'kama.html')

def mu(request):
    return render(request, 'mu.html')

def registration(request):
    return render(request, 'registration.html')\


def sundayschool(request):
    return render(request, 'sundayschool.html')

@login_required(login_url='login')
@superuser_only
def send_smss(request):
    return render(request, 'send_smss.html')

def youth(request):
    return render(request, 'youth.html')

def clusters(request):
    return render(request, 'clusters.html')

def teens(request): 
    return render(request, 'teens.html')

def meeting_calender(request):
    return render(request, 'meeting_calender.html')

def vicar_appointment_calender(request):
    return render(request, 'vicar_appointment_calender.html')

#updates an individual account in a database(personal profile update)
@login_required(login_url='login')
def update_account(request):
    form2 = UserNameForm( instance = request.user)
    form = UpdateUserForm( instance = request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance = request.user)
        if form.is_valid:
            form.save()
            messages.success(request, f'account updated succsesfully')
            return redirect('userhome')
    else:
        form = UpdateUserForm(instance = request.user)
    context = {'form':form , 'form2':form2}
    return render(request, 'update_account.html', context)

@login_required(login_url='login')
def update_group(request, user_id): 
    List = Account.objects.get(pk=user_id)
    form = UpdateGroupForm(instance = List)
    if request.method == 'POST':
        form = UpdateGroupForm(request.POST, instance = List)
        if form.is_valid:
            form.save()
            messages.success(request, f'group changed succsesfully')
            return redirect('superuser_home')
    else:
        form = UpdateGroupForm(instance = List)
    context = {'form':form , 'List':List}
    return render(request, 'update_group.html', context)

@login_required(login_url='login')
def dependent_group(request, account_id): 
    List = Dependent.objects.get(pk=account_id)
    form = UpdateGroupForm(instance = List)
    if request.method == 'POST':
        form = UpdateGroupForm(request.POST, instance = List)
        if form.is_valid:
            form.save()
            messages.success(request, f'group updated succsesfully')
            return redirect('superuser_home')
    else:
        form = UpdateGroupForm(instance = List)
    context = {'form':form , 'List':List}
    return render(request, 'dependent_group.html', context)

@login_required(login_url='login')
def view_info(request):
    List = request.user
    context = { 'List':List}
    return render(request, 'view_info.html', context)

@login_required(login_url='login')
def view_group(request):
    List = request.user
    context = { 'List':List}
    return render(request, 'view_group.html', context)

@login_required(login_url='login')
def dependent_register(request, account_id):
    List = Account.objects.get(pk=account_id)
    form = RegisterDependentForm()
    parent = List.membership_number
    if request.method == "POST": 
        form = RegisterDependentForm(request.POST)
        if form.is_valid():
                dependent = form.save(commit = False)
                dependent.parent1 = parent
                dependent.save()
                messages.success(request,"dependent added successfully")
                return redirect('account_list')
    else:
         form = RegisterDependentForm()
    context = {'form' : form , 'List' : List}
    return render(request, 'dependent_register.html', context)

@login_required(login_url='login')
@superuser_only
def superuser_edit(request, account_id):
    List = Account.objects.get(pk = account_id)
    form = EmailForm(request.POST, instance = List)
    if form.is_valid():
        form.save()
        messages.success(request,"Record Updated Successfully")
        return redirect('filter')
    context = {'List' : List}
    return render(request, 'superuser_edit.html', context)

@login_required(login_url='login')
@superuser_only
def emails(request):
    return render(request, 'emails.html')

@login_required(login_url='login')
@superuser_only
def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sendfrom = 'settings.EMAIL_HOST_USER'
        toaddress = [request.POST.get('email')]
        send_mail(subject,message,sendfrom,toaddress)
        return redirect('emails')
    return render(request, 'send_email.html')
def create_email(request):
   
    return render(request, 'send_email.html')


@login_required(login_url='login')
@superuser_only
def email_department(request):
    department = Department.objects.all()
    ministry = Ministry.objects.all()
    cluster = Cluster.objects.all()
    if request.method == 'POST':
        subject =request.POST.get('subject')
        message = request.POST.get('message')
        sendfrom = 'settings.EMAIL_HOST_USER'
        dept = request.POST.get('department_name')
        try:
           group1 = Department.objects.get(name = dept)
        except Department.DoesNotExist:
           group1 = None
        try:
           group2 = Cluster.objects.get(name = dept)
        except Cluster.DoesNotExist:
           group2 = None
        try:
           group3 = Ministry.objects.get(name = dept)
        except Ministry.DoesNotExist:
           group3 = None
        reciever1 = Account.objects.filter(department = group1)
        dependent_reciever1 = Dependent.objects.filter(department = group1)
        reciever2 = Account.objects.filter(department = group2)
        dependent_reciever2 = Dependent.objects.filter(department = group2)
        reciever3 = Account.objects.filter(department = group3)
        dependent_reciever3 = Dependent.objects.filter(department = group3)
        recievers1 = list(i for i in reciever1.values_list('email', flat=True) if bool(i))
        dependent_recepient1 = list(i for i in dependent_reciever1.values_list('dep_em', flat=True) if bool(i))
        recievers2 = list(i for i in reciever2.values_list('email', flat=True) if bool(i))
        dependent_recepient2 = list(i for i in dependent_reciever2.values_list('dep_em', flat=True) if bool(i))
        recievers3 = list(i for i in reciever3.values_list('email', flat=True) if bool(i))
        dependent_recepient3 = list(i for i in dependent_reciever3.values_list('dep_em', flat=True) if bool(i))
        recepient = recievers1 + dependent_recepient1 + recievers2 + dependent_recepient2 + recievers3 + dependent_recepient3
        send_mail(subject, message, sendfrom, recepient)
        return redirect('emails')
    context = {"department":department, "cluster":cluster, "ministry":ministry}
    return render(request, 'email_department.html', context)

@login_required(login_url='login')
@superuser_only
def send_all(request):
    if request.method == 'POST':
        subject =request.POST.get('subject')
        message = request.POST.get('message')
        sendfrom = 'settings.EMAIL_HOST_USER'
        reciever = []
        for user in Account.objects.all():
           reciever.append(user.email)
        recepient_dep = []
        for user in Dependent.objects.all():
           recepient_dep.append(user.mobile_number)
        recievers = recepient_dep + reciever
        send_mail(subject, message, sendfrom, recievers)
        return redirect('emails')
    return render(request, 'send_all.html')

@login_required(login_url='login')
@superuser_only
def church_accounts(request):
    List = Account.objects.all()
    return render(request, 'church_accounts.html',{'List' : List})

@login_required(login_url='login')
@superuser_only
def account_list(request):
    List = Account.objects.all()
    return render(request, 'account_list.html',{'List' : List})

@login_required(login_url='login')
def dependent_all(request):
    List = Dependent.objects.all()
    return render(request, 'dependent_all.html',{'List' : List})

@login_required(login_url='login')
def dependent_list(request):
    member = request.user.membership_number
    List = Dependent.objects.filter(parent1 = member )
    return render(request, 'dependent_list.html',{'List' : List})

#superuser can edit
@login_required(login_url='login')
@superuser_only
def account_edit(request, account_id):
    List = Account.objects.get(pk=account_id)
    form = EditUserForm(instance = List)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance = List)
        if form.is_valid():
            form.save()
            messages.success(request,"Account edited")
            return redirect('account_list')
    form = EditUserForm( instance = List)
    context = {'List':List, 'form':form}
    return render(request, 'account_edit.html',context )

@login_required(login_url='login')
def dependent_update(request, account_id):
    List = Dependent.objects.get(pk=account_id)
    form = EditDependentForm(instance = List)
    if request.method == "POST":
        form = EditDependentForm(request.POST, instance = List)
        if form.is_valid():
            form.save()
            messages.success(request,"Account edited")
            return redirect('dependent_list')
    form = EditDependentForm( instance = List)
    context = { 'List' : List , 'form':form}
    return render(request, 'dependent_update.html', context) 

@login_required(login_url='login')
@superuser_only
def superdependent_update(request, account_id):
    List = Dependent.objects.get(pk=account_id)
    form = EditDependentForm(instance = List)
    if request.method == "POST":
        form = EditDependentForm(request.POST, instance = List)
        if form.is_valid():
            form.save()
            messages.success(request,"Account edited")
            return redirect('dependent_all')
    form = EditDependentForm( instance = List)
    context = { 'List' : List, 'form':form }
    return render(request, 'superdependent_update.html', context) 

@login_required(login_url='login')
def dependent_view(request, account_id):
    List = Dependent.objects.get(pk=account_id)
    context = { 'List' : List }
    return render(request, 'dependent_view.html', context) 

@login_required(login_url='login')
@superuser_only
def delete_individual(request, account_id):
    List = Account.objects.get(pk = account_id)
    if request.method == "POST":
        List.delete()
        messages.error(request,"Account deleted")
        return redirect('account_list') 
    return render(request, 'delete_individual.html',{'List' : List})

@login_required(login_url='login')
@superuser_only
def dependent_delete(request, account_id):
    List = Dependent.objects.get(pk = account_id)
    if request.method == "POST":
        List.delete()
        return redirect('dependent_all')
    return render(request, 'delete_individual.html',{'List' : List})

@login_required(login_url='login')
def userhome(request):
    return render(request, 'userhome.html')
    
@login_required(login_url='login')
@superuser_only
def filter_all(request):
    qs = Account.objects.all()
    qa = Dependent.objects.all()
    search = request.GET.get('search')
    if search !='' and search is not None:
        qs = qs.filter( Q(membership_number = search)) . distinct()
    if search !='' and search is not None:
        qa = qa.filter( Q(membership_number__icontains = search)) . distinct()
    context = {'queryset' : qs , 'query':qa}
    return render(request, 'filter_all.html', context)

@login_required(login_url='login')
@superuser_only
def filter(request):
    qs = Account.objects.all()
    search = request.GET.get('search')
    if search !='' and search is not None:
        qs = qs.filter(Q(last_name__icontains = search) | Q(first_name__icontains = search)|Q(email__icontains = search) | Q(mobile_number__icontains = search)| Q(membership_number__icontains = search)) . distinct()
    context = {'queryset' : qs }
    return render(request, 'filter.html', context)

@login_required(login_url='login')
@superuser_only
def dependent_filter(request):
    qs = Dependent.objects.all()
    search = request.GET.get('search')
    if search !='' and search is not None:
        qs = qs.filter(Q(last_name__icontains = search) | Q(first_name__icontains = search)|Q(dep_em__icontains = search) | Q(mobile_number__icontains = search)| Q(membership_number__icontains = search)) . distinct()
    context = {'queryset' : qs}
    return render(request, 'dependent_filter.html', context) 

@login_required(login_url='login')
@superuser_only
def group_members(request):
    department = Department.objects.all()
    ministry = Ministry.objects.all()
    cluster = Cluster.objects.all()
    qs = Account.objects.all()
    qa = Dependent.objects.all()
    group = request.GET.get('group')
    if group !='' and group is not None:
        qa = qa.filter(Q(department__name__icontains  = group)| Q(cluster__name__icontains = group)|Q(ministry__name__icontains = group)). distinct()
    if group !='' and group is not None:    
        qs = qs.filter(Q(department__name__icontains  = group)| Q(cluster__name__icontains = group)|Q(ministry__name__icontains = group)). distinct()
    if group is None:
        qs = None
        qa = None

    context = {'queryset' : qs ,'query':qa, 'department':department, 'ministry':ministry, 'cluster':cluster}
    return render(request, 'group_members.html', context)

@login_required(login_url='login')
def edit(request):
    return render(request, 'edit.html')

@login_required(login_url='login')
def userhome(request):
    return render(request, 'userhome.html')


@login_required(login_url='login')
@superuser_only
def superuser_home(request):
    return render(request, 'superuser_home.html')


@login_required(login_url='login')
def admin_home(request):
    return render(request, 'admin_home.html')

@login_required(login_url='login')
@superuser_only
def change_group(request,):
    List = Account.objects.all()
    return render(request, 'change_group.html', {'List':List})
    
@login_required(login_url='login')
@superuser_only
def make_superuser(request, account_id):
    perm = 'superuser'
    List = Account.objects.get(pk=account_id)
    user = List
    group = Group.objects.get(name = 'user')
    user.groups.remove(group)
    group = Group.objects.get(name = 'admin')
    user.groups.remove(group)
    group = Group.objects.get(name = 'superuser')
    group.user_set.add(user)
    context = {'List' : List , 'perm':perm }
    return render(request, 'change_usergroup.html', context )
    

@login_required(login_url='login')
@superuser_only
def make_admin(request, account_id):
    perm = 'admin'
    List = Account.objects.get(pk=account_id)
    user = List
    group = Group.objects.get(name = 'admin')
    group.user_set.add(user)
    messages.success(request,"Account edited")
    context = {'List' : List , 'perm':perm }
    return render(request, 'change_usergroup.html', context )

@login_required(login_url='login')
@superuser_only
def make_user(request, account_id):
    group = 'user'
    List = Account.objects.get(pk=account_id)
    user = List
    group = Group.objects.get(name = 'admin')
    user.groups.remove(group)
    group = Group.objects.get(name = 'superuser')
    user.groups.remove(group)
    group = Group.objects.get(name = 'user')
    group.user_set.add(user)
    messages.success(request,"Account edited")
    context = {'List' : List , 'group':group }
    return render(request, 'change_usergroup.html', context )

#new register/ CREATION\
@csrf_exempt
@login_required(login_url='login')
@superuser_only
def register(request):
        user = request.user.id
        initial_data={'mobile_number': "+2547"}
        form = CreateUserForm( initial = initial_data)
        if request.method == "POST":
            form = CreateUserForm(request.POST , initial=initial_data)
            if form.is_valid():
                user = form.save(commit = False)
                account = form.cleaned_data.get('first_name')
                mobile_number = form.cleaned_data.get('mobile_number')
                email = form.cleaned_data.get('email') 
                user.save()
                member =  Account.objects.get(email = email)
                membership_number = member.membership_number
                subject = 'Password Change'
                from_email = 'settings.EMAIL_HOST_USER'
                to = email
                plaintext = get_template('email.txt')
                htmly     = get_template('email.html')
                context = { 'membership_number': membership_number, 'account':account }
                text_content = plaintext.render(context)
                html_content = htmly.render(context)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send() 
                username = settings.AT_USER_NAME   
                api_key = settings.AT_API_KEY      
                africastalking.initialize(username, api_key)
                sms = africastalking.SMS
                recepients = [mobile_number]
                message =  "Check your email to change password, Your membership number is: " + membership_number
                sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)

                #send_activation_email(user,request)
                group = Group.objects.get(name = 'user')
                user.groups.add(group)
                messages.success(request,'Account was successfully  created for ' +account)
                return redirect('superuser_home')
        context= {'form' : form }
        return render(request, 'register.html', context)

def register_manual(request):
        user = request.user.id
        initial_data={'mobile_number': "+2547" , 'password1': "ACKWENDANI001" , 'password2': "ACKWENDANI001"}
        form = CreateUserManualForm( initial = initial_data)
        password = "ACKWENDANI@2022"
        if request.method == "POST":
            form = CreateUserManualForm(request.POST , initial=initial_data)
            if form.is_valid():
                user = form.save(commit = False)
                account = form.cleaned_data.get('first_name')
                member = form.cleaned_data.get('membership_number')
                number = form.cleaned_data.get('mobile_number')
                email = form.cleaned_data.get('email')
                user.save()
                username = settings.AT_USER_NAME   
                api_key = settings.AT_API_KEY      
                africastalking.initialize(username, api_key)
                sms = africastalking.SMS
                recepients = [number]
                message =  "Check your email to change password,,,, Your membership number is: " +member
                sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)
                subject = 'Password Change'
                from_email = 'settings.EMAIL_HOST_USER'
                to = email
                plaintext = get_template('email.txt')
                htmly     = get_template('email.html')
                context = { 'membership_number': member, 'account':account }
                text_content = plaintext.render(context)
                html_content = htmly.render(context)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()  

                #send_activation_email(user,request)
                group = Group.objects.get(name = 'user')
                user.groups.add(group)
                messages.success(request,'Account was successfully  created for ' +account)
                return redirect('superuser_home')
        context= {'form' : form,'password':password}
        return render(request, 'register_manual.html', context)

@csrf_exempt
def sendEmail(request):
    return render(request , 'confirm_template.html')

def profile(request):
    List = request.user
    List1 = Dependent.objects.filter(parent1 = List.membership_number)
    department = Department.objects.filter(account = request.user)
    ministry = Ministry.objects.filter(account = request.user)
    cluster = Cluster.objects.filter(account = request.user)
    context= {'List' : List, 'List1':List1, 'department':department, 'ministry':ministry, 'cluster':cluster}
    return render(request , 'profile.html', context)

@unauthenticated_user
def login(request):
    if request.method == "POST":
        membership_number = request.POST.get('membership_number')
        password = request.POST.get('password')
        user = authenticate(request, username = membership_number, password = password)
        

        if user is not None:
            logsin(request, user)
            return redirect('superuser_home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context= {}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def baptism(request):
    form = BaptismRegistrationForm(request.POST)
    if request.method == "POST":
        form = BaptismRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request,"form saved")
            return redirect('forms')
    form = BaptismRegistrationForm(request.POST) 
    context = {'form' : form}
    return render(request, 'baptism.html', context) 

@login_required(login_url='login')
def wedding(request):
    form = WeddingRegistrationForm(request.POST)
    if request.method == "POST":
        form = WeddingRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request,"form added")
            return redirect('forms')
    form = WeddingRegistrationForm(request.POST) 
    context = {'form' : form}
    return render(request, 'wedding.html', context)



@login_required(login_url='login')
def dept_form(request):
    form = DepartmentForm( instance = request.user)
    #List = account.objects.get( pk = request.user.id )
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance = request.user)
        if form.is_valid:
            form.save()
    else:
        form = DepartmentForm(instance = request.user)
    context = {'form' : form }
    return render(request, 'dept_form.html', context)

@login_required(login_url='login')
def communion(request):
    form = CommunionRegistrationForm(request.POST)
    if request.method == "POST":
        form = CommunionRegistrationForm(request.POST)
        messages.success(request,"form added")
        return redirect('forms')
    form = CommunionRegistrationForm(request.POST) 
    context = {'form' : form}
    return render(request, 'communion.html', context)

@login_required(login_url='login')
def admin_cluster(request):
    return render(request, 'admin_cluster.html')

@login_required(login_url='login')
def admin_department(request):
    return render(request, 'admin_department.html')

@login_required(login_url='login')
def admin_talent(request):
    return render(request, 'admin_talent.html')

@login_required(login_url='login')
def department_view(request):
    manager = request.user.id
    manager_group =  Account.department.through.objects.get(account_id = manager)
    m_id = manager_group.department
    List = Account.objects.all().filter(department = m_id)
    Lists = Dependent.objects.all().filter(department = m_id)
    return render(request, 'department_view.html', {'List' : List , 'Lists':Lists})

@login_required(login_url='login')
def department_adminemail(request):
    if request.method == 'POST':
        subject =request.POST.get('subject')
        message = request.POST.get('message')
        sendfrom = 'settings.EMAIL_HOST_USER'
        manager = request.user.id
        manager_group =  Account.department.through.objects.get(account_id = manager)
        m_id = manager_group.department
        department = m_id
        try:
           group = Department.objects.get(name = department)
        except Department.DoesNotExist:
           group = None
        reciever = Account.objects.filter(department = group)
        recievers = list(i for i in reciever.values_list('email', flat=True) if bool(i))
        dependent_reciever = Dependent.objects.filter(department = group)
        dependent_recepient = list(i for i in dependent_reciever.values_list('dep_em', flat=True) if bool(i))
        recepient = recievers + dependent_recepient
        send_mail(subject, message, sendfrom, recepient)
        return redirect('admin_department')
    return render(request, 'adminemail.html')

@login_required(login_url='login')
def department_adminsms(request):
    if request.method == 'POST':
       username = settings.AT_USER_NAME   
       api_key = settings.AT_API_KEY      
       africastalking.initialize(username, api_key)
       sms = africastalking.SMS
       manager = request.user.id
       manager_group =  Account.department.through.objects.get(account_id = manager)
       m_id = manager_group.clusdepartmentter
       try:
           group = Department.objects.get(name = m_id)
       except Department.DoesNotExist:
           group = None
       reciever = Account.objects.filter(department = group)
       dependent_reciever = Dependent.objects.filter(department = group)
       recepient = list(i for i in reciever.values_list('mobile_number', flat=True) if bool(i))
       dependent_recepient = list(i for i in dependent_reciever.values_list('mobile_number', flat=True) if bool(i))
       recepients = recepient + dependent_recepient
       message = request.POST.get('message')
       sms.send(message ,recepients, sender_id = settings.AT_FROM_VALUE)
       return redirect('admin_department')
    else:
        return render(request, "adminsms.html")

@login_required(login_url='login')
def add_department(request):
    return render(request, "add_department.html")

@login_required(login_url='login')
def dept_add(request):
    group = "Department"
    form = AddDepartmentForm(request.POST)
    if request.method == "POST":
        form = AddDepartmentForm(request.POST)
        form.save()
        messages.success(request,"group added")
        return redirect('superuser_home')
    form = AddDepartmentForm(request.POST) 
    context = {'form' : form , 'group':group}
    return render(request, 'group_add.html', context)

@login_required(login_url='login')
@superuser_only
def group_list(request):
    List = Department.objects.all()
    context = {'List' : List }
    return render(request, 'group_list.html', context)

@login_required(login_url='login')
@superuser_only
def delete_dept(request, group_id):
    List = Department.objects.get(pk = group_id)
    if request.method == "POST":
        List.delete()
        return redirect('group_list')
    return render(request, 'delete_group.html',{'List' : List})

@login_required(login_url='login')
@superuser_only
def edit_dept(request, group_id):
    List = Department.objects.get(pk=group_id)
    form = AddDepartmentForm()
    if request.method == "POST":
        form = AddDepartmentForm(request.POST, instance = List)
        if form.is_valid():
            form.save()
            messages.success(request,"Account edited")
            return redirect('group_list')
    return render(request, 'group_edit.html',{'List' : List})

  
def success(request):
    return HttpResponse('successfully uploaded')

@login_required(login_url='login')
@superuser_only
def add_staffmember(request):
    form = AddStaffMemberForm()
    if request.method == 'POST':
        form = AddStaffMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Staff member added")
            return redirect('superuser_home')
            
    else:
        form = AddStaffMemberForm()
    return render(request, 'add_staffmember.html', {'form': form})

def staff_members(request):
    staffmember = StaffMember.objects.all() 
    return render(request, 'staff_members.html', {'staffmember' : staffmember})

@login_required(login_url='login')
@superuser_only
def excel_uploadattendance(request):
    if request.method == 'POST':
        attendance_resource = AttendanceResource()
        dataset = Dataset()
        attendance = request.FILES['myfile']
        if not attendance.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'excel_uploadattendance.html')
        imported_data = dataset.load(attendance.read(), format = 'xlsx')
        for data in imported_data:
            value = Attendance(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
            )
            value.save()
            messages.info(request, 'form uploaded')
        return redirect('userhome')
    else:
        return render(request, 'excel_uploadattendance.html')

@login_required(login_url='login')
@superuser_only
def email_noattendance(request):
    if request.method == 'POST':
        datetoday  = date.today()
        d1 = datetoday.strftime("%Y-%m-%d")
        subject ='No Attendance'
        message = 'We did not see you in church, kindly purpose to attend'
        sendfrom = 'settings.EMAIL_HOST_USER'
        recievers = []
        for account in Attendance.objects.filter(date_of_attendance = d1):
           recievers.append(account.email)
        total = []
        for account in Account.objects.all():
            total.append(account.email)
        reciever = list(set(recievers).symmetric_difference(set(total)))
      
        send_mail(subject, message, sendfrom, reciever, fail_silently=False)
        return redirect('superuser_home')
    return render(request, 'message_noattendance.html')


@login_required(login_url='login')
@superuser_only
def message_noattendance(request):
    username = settings.AT_USER_NAME   
    api_key = settings.AT_API_KEY      
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    if request.method == 'POST':
        datetoday  = date.today()
        d1 = datetoday.strftime("%Y-%m-%d")
        message = ' you missed yesterday'
        recievers = []
        for account in Attendance.objects.filter(date_of_attendance = d1):
           recievers.append(account.mobile_number)
        total = []
        for account in Account.objects.all():
            total.append(account.mobile_number)
        reciever = list(set(recievers).symmetric_difference(set(total)))
        response = sms.send(message ,reciever, sender_id = settings.AT_FROM_VALUE)
        return redirect('superuser_home')
    return render(request, 'message_noattendance.html')



@login_required(login_url='login')
@superuser_only
def add_activity(request):
    form = AddChurchActivityForm()
    if request.method == 'POST':
        form = AddChurchActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser_home')
    else:
        form = AddChurchActivityForm()
    context = {'form':form}
    return render(request, 'add_activity.html', context)

@login_required(login_url='login')
def event_application(request):
    form = EventApplicationForm()
    if request.method == 'POST':
        form = EventApplicationForm(request.POST)
        if form.is_valid():
            name = form.save(commit = False)
            name.name = request.user
            name.application = 'pending'
            name.save()
            messages.success(request,"event updated successfully")
            return redirect('userhome')
    else:
        form = EventApplicationForm()
    context = {'form':form}
    return render(request, 'event_application.html', context)

@login_required(login_url='login')
def application_satus(request):
    current = request.user
    app = EventApplication.objects.filter(name_id=current).all()
    context = { 'app':app }
    return render(request,'application_satus.html',context)

@login_required(login_url='login')
def appplication_page(request):
    user = request.user.id
    user_name =  Account.objects.get(account_id = user)
    use = user_name.email
    app = EventApplication.objects.filter(email=use).all()
    context = { 'app':app }
    return render(request,'application_page.html',context)

@login_required(login_url='login')
def user_application(request):
    return render(request, 'user_application.html')


@login_required(login_url='login')
def view_event(request):
    List = ChurchActivity.objects.all()
    return render(request, 'view_event.html', {'List':List})

@login_required(login_url='login')
@superuser_only
#admin views status
def superuser_application(request):
    app = EventApplication.objects.filter(application = 'pending').all()
    context = { 'app':app }
    return render(request, 'superuser_application.html', context)

@login_required(login_url='login')
@superuser_only
def application_accept(request, app_id):
    app = EventApplication.objects.get(pk = app_id)
    app.application = 'accepted'
    app.save()
    event_name = app.event_name
    subject = 'Application Accepted'
    sendfrom = 'settings.EMAIL_HOST_USER'
    recepient = Account.objects.get(email__iexact = app.name)
    toaddress = [recepient.email]
    if event_name == 'baptism':
       message = 'Your application was accepted. Click on the following link to fill in the form, <a href="http://127.0.0.1:8000/baptism/">Click</a>'
       send_mail(subject,message,sendfrom,toaddress)
       messages.success(request,"Event was updated successfully")
       return render(request, 'superuser_home.html')
    elif event_name == 'communion':
       message = 'Your application was accepted. Click on the following link to fill in the form, <a href="http://127.0.0.1:8000/communion/">Click</a>'
       send_mail(subject,message,sendfrom,toaddress)
       messages.success(request,"Event was updated successfully")
       return render(request, 'superuser_home.html')
    elif event_name == 'wedding':
       message = 'Your application was accepted. Click on the following link to fill in the form, <a href="http://127.0.0.1:8000/wedding/">Click</a>'
       send_mail(subject,message,sendfrom,toaddress)
       messages.success(request,"Event was updated successfully")
       return render(request, 'superuser_home.html')
    else:
       messages.success(request,"Event was updated successfully")
       return render(request, 'superuser_home.html')


@login_required(login_url='login')
@superuser_only
def application_reject(request, app_id):
    app = EventApplication.objects.get(pk = app_id)
    app.application = 'rejected'
    app.save()
    messages.success(request,"Event was updated successfully")
    return render(request, 'superuser_home.html')
