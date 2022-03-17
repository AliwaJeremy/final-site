from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.fields import DateField
from django.forms.widgets import CheckboxSelectMultiple
from ackweb.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import *
from django import forms

 
User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(UserCreationForm):
  genders = (('Male','Male'),('Female','Female'))
  gender=forms.ChoiceField(label='Gender', choices=genders, widget=forms.RadioSelect)
  title1 = 'Dr'
  title2 = 'Mr'
  title3 = 'Mrs'
  title4 = 'Tr'
  TITLE_CHOICES = (
        (title1, u"Dr"),
        (title2, u"Mr"),
        (title3, u"Mrs"),
        (title4, u"Tr"),
    )
  title = forms.ChoiceField(choices=TITLE_CHOICES)

  status1 = 'Married in Church'
  status2 = 'Customary Marriage'
  status3 = 'Civil Marriage'
  status4 = 'Widow'
  status5 = 'Widower'
  status6 = 'Divorced'
  status7 = 'Seperated'
  status8 = 'Single'
  STATUS_CHOICES = (
        (status1, u"Married in Church"),
        (status2, u"Customary Marriage"),
        (status3, u"'Civil Marriage"),
        (status4, u"Widow"),
        (status5, u"Widower"),
        (status6, u"Divorced"),
        (status7, u"Seperated"),
        (status8, u"Single"),
    )
  marital_status = forms.ChoiceField(choices=STATUS_CHOICES)

  church1 = 'Baptized'
  church2 = 'Confirmed'
  church3 = 'Communicant'
  CHURCH_CHOICES = (
        (church1, u"Baptized"),
        (church2, u"Confirmed"),
        (church3, u"Communicant"),
    )
  church_status = forms.ChoiceField(choices=CHURCH_CHOICES)
  department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  cluster = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  ministry = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )

  date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Must be at least 18 years old to register')
        return dob
  mobile_number = forms.CharField()
  def clean_mobile_number(self):
        number = self.cleaned_data['mobile_number']
        if len(number) != 13:
            raise forms.ValidationError('Please Enter a valid Phone Number')
        return number
  def clean_password(self):
        password = self.cleaned_data['password1']
        if password is None:
            raise forms.ValidationError('Please enter a password')
        return password

  class Meta:
    model = Account
    fields = [ 'email', 'first_name' , 'last_name' , 'mobile_number', 'id_number' ,  'date_of_birth' ,
     'profession', 'title', 'gender', 'marital_status', 'church_status', 'address' , 'department', 'cluster','ministry'
    , 'password1','password2' ]
     
class CreateUserManualForm(UserCreationForm):
  genders = (('Male','Male'),('Female','Female'))
  gender=forms.ChoiceField(label='Gender', choices=genders, widget=forms.RadioSelect)
  title1 = 'Dr'
  title2 = 'Mr'
  title3 = 'Mrs'
  title4 = 'Tr'
  TITLE_CHOICES = (
        (title1, u"Dr"),
        (title2, u"Mr"),
        (title3, u"Mrs"),
        (title4, u"Tr"),
    )
  title = forms.ChoiceField(choices=TITLE_CHOICES)

  status1 = 'Married in Church'
  status2 = 'Customary Marriage'
  status3 = 'Civil Marriage'
  status4 = 'Widow'
  status5 = 'Widower'
  status6 = 'Divorced'
  status7 = 'Seperated'
  status8 = 'Single'
  STATUS_CHOICES = (
        (status1, u"Married in Church"),
        (status2, u"Customary Marriage"),
        (status3, u"'Civil Marriage"),
        (status4, u"Widow"),
        (status5, u"Widower"),
        (status6, u"Divorced"),
        (status7, u"Seperated"),
        (status8, u"Single"),
    )
  marital_status = forms.ChoiceField(choices=STATUS_CHOICES)

  church1 = 'Baptized'
  church2 = 'Confirmed'
  church3 = 'Communicant'
  CHURCH_CHOICES = (
        (church1, u"Baptized"),
        (church2, u"Confirmed"),
        (church3, u"Communicant"),
    )
  church_status = forms.ChoiceField(choices=CHURCH_CHOICES)
  department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  cluster = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  ministry = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Must be at least 18 years old to register')
        return dob
  mobile_number = forms.CharField()
  def clean_mobile_number(self):
        number = self.cleaned_data['mobile_number']
        if len(number) != 13 :
            raise forms.ValidationError('Please Enter a valid Phone Number')
        return number
  password1 = forms.CharField(widget=forms.PasswordInput,initial="ACKWENDANI@2022") 
  password2 = forms.CharField(widget=forms.PasswordInput, initial="ACKWENDANI@2022")
  class Meta:
    model = Account
    fields = [ 'email', 'first_name' , 'last_name' , 'mobile_number', 
    'id_number' ,  'date_of_birth' , 'profession', 'title', 'gender', 'marital_status', 
    'church_status', 'address' , 'department' , 'cluster','ministry' ,'membership_number', 
    'password1','password2' ]

     
class UpdateUserForm(ModelForm):
  class Meta:
    model = Account
    fields = [  'first_name' , 'last_name' , 'email' , 'mobile_number' , 'address' ]
 

class UpdateGroupForm(ModelForm):
  department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  cluster = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  ministry = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  class Meta:
    model = Account
    fields = [  'department' , 'cluster' , 'ministry' ]
  

class AddDepartmentForm(forms.ModelForm):
  class Meta:
    model = Department
    fields = [  'name'  ]

class AddClusterForm(forms.ModelForm):
  class Meta:
    model = Cluster
    fields = [  'name'  ]

class AddMinistryForm(forms.ModelForm):
  class Meta:
    model = Ministry
    fields = [  'name'  ]
  
#superuser update
class EditUserForm(forms.ModelForm): 
  department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  cluster = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  ministry = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  class Meta:
    model = Account
    fields = [ 'email', 'first_name' , 'last_name' , 'mobile_number'  ,'department','ministry', 'cluster' ]

class DepartmentForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
       super(DepartmentForm, self).__init__(*args, **kwargs)
       self.fields['email'].widget.attrs['readonly'] = True
       self.fields['first_name'].widget.attrs['readonly'] = True
       self.fields['last_name'].widget.attrs['readonly'] = True
       self.fields['mobile_number'].widget.attrs['readonly'] = True
  class Meta:
    model = Account
    fields = [ 'email', 'first_name' , 'last_name' , 'mobile_number']

class UserNameForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = [ 'last_name'  ]



class EmailForm(forms.ModelForm):
    subject = forms.CharField(
                        label='subject',
                        max_length=100,
                        min_length=3,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'start with country code e.g +254xxx '}))  # noqa: E501
    message = forms.CharField(
                        label='message',
                        max_length=255,
                        min_length=3,
                        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 20}))
 

class RegisterDependentForm(forms.ModelForm):
  genders = (('Male','Male'),('Female','Female'))
  gender=forms.ChoiceField(label='Gender', choices=genders, widget=forms.RadioSelect)
  relationship1 = 'Spouse'
  relationship2 = 'Son'
  relationship3 = 'Daughter'
  RELATIONSHIP_CHOICES = (
        (relationship1, u"Spouse"),
        (relationship2, u"Son"),
        (relationship3, u"Daughter"),
    )
  relationship = forms.ChoiceField(choices=RELATIONSHIP_CHOICES)
  church1 = 'Baptized'
  church2 = 'Confirmed'
  church3 = 'Communicant'
  CHURCH_CHOICES = (
        (church1, u"Baptized"),
        (church2, u"Confirmed"),
        (church3, u"Communicant"),
    )
  church_status = forms.ChoiceField(choices=CHURCH_CHOICES)
  department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  cluster = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  ministry = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
  date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  mobile_number = forms.CharField()
  def clean_mobile_number(self):
        number = self.cleaned_data['mobile_number']
        if len(number) != 13:
            raise forms.ValidationError('Please Enter a valid Phone Number')
        return number
  def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Birth date is invalid')
        return dob
  class Meta:
    model = Dependent
    fields = [
       'first_name', 'last_name' ,  'dep_em' , 'gender' , 'id_number' , 'date_of_birth' , 'relationship' , 'mobile_number', 'membership_email', 'church_status' ,'parent2', 'department', 'cluster', 'ministry'

    ]
    exclude = ['membership_email']
    
    
    widgets = {
            'date_of_birth': DateInput(),
        }
    

class EditDependentForm(forms.ModelForm):
  class Meta:
    model = Dependent
    fields = [
       'first_name', 'last_name' ,  'dep_em' , 'mobile_number',
    ]
  

class BaptismRegistrationForm(forms.ModelForm):
  areparents_baptised = (('Yes','Yes'),('No','No'))
  parents_baptised=forms.ChoiceField( choices=areparents_baptised, widget=forms.RadioSelect)
  areparents_members = (('Yes','Yes'),('No','No'))
  parents_members=forms.ChoiceField( choices=areparents_members, widget=forms.RadioSelect)
  date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)
  def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Must be at least 18 years old to register')
        return dob
  class Meta:
    model = Baptism
    fields = [ 
      'name','date_of_birth','date_of_baptism','christian_name','father_name','mother_name','guardian_name','parent_postal_address','mobile_number_father',
    'mobile_number_mother','residential_address','date_of_marriage','place_of_marriage','parents_baptised','parents_members',
    ]
    date_of_baptism = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_of_marriage = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    widgets = {
            'date_of_birth': DateInput(),
            'date_of_baptism': DateInput(),
            'r': DateInput(),
        }
  
class WeddingRegistrationForm(forms.ModelForm):
  class Meta:
    model = Wedding
    fields = [ 
      'husband_name','mobile_number_husband' ,'husband_dob','husband_date_of_baptism','wife_name','wife_dob','wife_date_of_baptism','mobile_number_wife',
      'H_father_name' ,'H_mother_name','W_father_name','W_mother_name','guardian_name','postal_address','residential_address','date_of_marriage',]
    husband_dob = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    husband_date_of_baptism = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    wife_dob = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    wife_date_of_baptism = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_of_marriage = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    widgets = {
            'husband_dob': DateInput(),
            'husband_date_of_baptism': DateInput(),
            'wife_dob': DateInput(),
            'wife_date_of_baptism': DateInput(),
            'date_of_marriage': DateInput(),
        }

class CommunionRegistrationForm(forms.ModelForm):
  class Meta:
    model = Communion
    fields = [ 
      'name', 'mobile_number','dob','date_of_communion','postal_address','residential_address'
    ]
    dob = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_of_communion = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    widgets = {
            'date_of_communion': DateInput(),
        }


class AddChurchActivityForm(forms.ModelForm):
  class Meta:
    model = ChurchActivity
    fields = [ 
     'name' , 'date' ,'group' ,
    ]
    date = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    widgets = {
            'date': DateInput(),
        }

class EventApplicationForm(forms.ModelForm):
  class Meta:
    model = EventApplication
    fields = [ 
     'event_name' ,'description'
    ]

class AddStaffMemberForm(forms.ModelForm):
  mobile_number = forms.CharField()
  def clean_mobile_number(self):
        number = self.cleaned_data['mobile_number']
        if len(str(number)) != 13:
            raise forms.ValidationError('Please Enter a valid Phone Number')
        return number
  class Meta:
    model = StaffMember
    fields = [ 
      'name','category', 'mobile_number','email','information','image'
    ]

class AttendanceForm(forms.ModelForm):
  class Meta:
    model = Attendance
    fields = [ 
      'name', 'date_of_attendance' , 'temperature', 'mobile_number'
    ]

class CreateSms(forms.Form):
    phone_number = forms.CharField(
                        label='phone number',
                        max_length=100,
                        min_length=3,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'start with country code e.g +254xxx '}))  # noqa: E501
    message = forms.CharField(
                        label='message',
                        max_length=255,
                        min_length=3,
                        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 20}))  # noqa: E501
                    
                    
