from email.policy import default
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models, transaction
from django.db.models.deletion import CASCADE, RESTRICT, SET_NULL
from django.conf import settings
from django.http import request
import requests
import uuid
import africastalking


#create a new user
#create superuser

class MyAccountManager(BaseUserManager):
    def create_user(self, membership_number, email,mobile_number, password=None):
        if not membership_number:
            raise ValueError("Membership Number is required")
        if not email:
            raise ValueError("Users must have an email.")
        if not mobile_number:
            raise ValueError("Users must have a phone number.")
        user = self.model(
            membership_number=membership_number,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, mobile_number, membership_number, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            mobile_number = mobile_number,
            password = password,
            membership_number = membership_number,        
        )
        user.is_admin =  True
        user.is_staff =  True
        user.is_superuser =  True

        user.save(using = self._db)


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="name", max_length=255)
    theme = models.CharField(verbose_name="theme", max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    

    def __str__(self):
       return self.name


class Cluster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="name", max_length=255)
    theme = models.CharField(verbose_name="theme", max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    

    def __str__(self):
       return self.name

class Ministry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="name", max_length=255)
    theme = models.CharField(verbose_name="theme", max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    

    def __str__(self):
       return self.name


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique = True)
    username = models.CharField(verbose_name = "username", max_length=30, blank=True, null=True, default = email)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="first name", max_length=255)
    last_name = models.CharField(verbose_name="last name", max_length=255)
    mobile_number = models.CharField(verbose_name="mobile number", max_length=255, unique = True)
    id_number = models.CharField(verbose_name="id number", max_length=255 )
    password = models.CharField(verbose_name="password", max_length=255)
    date_of_birth = models.DateField(verbose_name="date of birth", blank=True, null=True)
    address = models.CharField(verbose_name="address", max_length=255, blank=True, null=True)
    profession = models.CharField(verbose_name="profession", max_length=255, blank=True, null=True)
    title = models.CharField(verbose_name="title", max_length=255, blank=True, null=True)
    gender = models.CharField(verbose_name="gender", max_length=255, blank=True, null=True)
    marital_status = models.CharField(verbose_name="marital status", max_length=255, blank=True, null=True)
    church_status = models.CharField(verbose_name="church status", max_length=255, blank=True, null=True)
    id = models.AutoField(primary_key=True, editable=False)
    membership_number = models.CharField(verbose_name="Membership number", max_length=255, unique = True )
    department = models.ManyToManyField(Department, blank=True)
    cluster = models.ManyToManyField(Cluster, blank=True)
    ministry = models.ManyToManyField(Ministry,blank=True)
    is_email_verified = models.BooleanField(default = False)

    def update_membno(self):
        if not self.membership_number:
            test_id = Account.objects.get(pk=self.id).id
            member_no = 200 + test_id
            Account.objects.filter(id=test_id).update(membership_number="ACKWE%05d" % member_no)
                   

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        self.update_membno()

    

    objects = MyAccountManager()

    USERNAME_FIELD = 'membership_number'
    REQUIRED_FIELDS = ['email','mobile_number']
    
    
    @property
    def family_number(self):
        return "%s" % self.membership_number + "01"

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return  self.membership_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Dependent(models.Model):
    
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    dep_em = models.EmailField(verbose_name="Dependent Email", max_length=60, unique = True)
    gender = models.CharField(verbose_name="gender", max_length=255, blank=True, null=True)
    id_number = models.CharField(verbose_name="ID Number", max_length=255, unique = True)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    relationship = models.CharField(verbose_name="relationship", max_length=255, blank=True, null=True)
    profession = models.CharField(verbose_name="profession", max_length=255, blank=True, null=True)
    church_status = models.CharField(verbose_name="church status", max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name="address", max_length=255, blank=True, null=True)
    mobile_number = models.CharField(verbose_name="Mobile Number" , max_length=255, default = "+2457", unique = True)
    department = models.ManyToManyField(Department, blank=True)
    cluster = models.ManyToManyField(Cluster, blank=True)
    ministry = models.ManyToManyField(Ministry, blank=True)
    id = models.AutoField(verbose_name="membership number",primary_key=True)
    parent1 = models.CharField( max_length=255,verbose_name="First Parent", default = "1")
    parent2 = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name="Second Parent" ,blank=True, null=True)
    membership_number = models.CharField( max_length=255,verbose_name="Membership Number",unique = True)

    def update_membno(self):
        if not self.membership_number:
            test_id = Dependent.objects.get(pk=self.id).id
            total = Dependent.objects.filter(parent1__contains=self.parent1).count()
            idno = total+1
            Dependent.objects.filter(id=test_id).update(membership_number=self.parent1 + "%02d" % idno)

    def save(self, *args, **kwargs):
        super(Dependent, self).save(*args, **kwargs)
        self.update_membno()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=60, blank=True, null=True) 
    membership_number = models.CharField(verbose_name="Mebership Number", max_length=255, blank=True, null=True)
    date_of_attendance = models.DateField(verbose_name="Date of Attendance", blank=True, null=True)
    temperature = models.IntegerField(verbose_name="Temperature", blank=True, null=True)
    mobile_number = models.CharField(verbose_name="Mobile Number", max_length=255, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.name, self.date_of_attendance)


class Baptism(models.Model):
    name = models.CharField(verbose_name="name", max_length=255)
    date_of_birth = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    date_of_baptism = models.DateField(verbose_name="Date of Baptism", blank=True, null=True)
    christian_name = models.CharField(verbose_name="Christian Name", max_length=255)
    father_name = models.CharField(verbose_name="Father Name", max_length=255)
    mother_name = models.CharField(verbose_name="Mother Name", max_length=255)
    guardian_name = models.CharField(verbose_name="Guardian Name", max_length=255)
    parent_postal_address = models.CharField(verbose_name="Address", max_length=255)
    mobile_number_father = models.CharField(verbose_name="Father Mobile Number", max_length=255, blank=True, null=True)
    mobile_number_mother = models.CharField(verbose_name="Mother Mobile Number", max_length=255, blank=True, null=True)
    residential_address = models.CharField(verbose_name="Residential Address", max_length=255, blank=True, null=True)
    date_of_marriage = models.DateField(verbose_name="Date of Marriage", blank=True, null=True)
    place_of_marriage = models.CharField(verbose_name="Place of Marriage", max_length=255, blank=True, null=True)
    parents_baptised = models.CharField(verbose_name="Parents Baptised?", max_length=255, blank=True, null=True)
    parents_members = models.CharField(verbose_name="Parents Members?", max_length=255, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.name, self.name)



class Wedding(models.Model):
    husband_name = models.CharField(verbose_name="Husband name", max_length=255)
    mobile_number_husband = models.CharField(verbose_name="Husband Mobile Number", max_length=255, blank=True, null=True)
    husband_dob = models.DateField(verbose_name="Husband DoB", blank=True, null=True)
    husband_date_of_baptism = models.DateField(verbose_name="H. Date of Baptism", blank=True, null=True)
    wife_name = models.CharField(verbose_name="Wife name", max_length=255)
    wife_dob = models.DateField(verbose_name="Wife DoB", blank=True, null=True)
    wife_date_of_baptism = models.DateField(verbose_name="W. Date of Baptism", blank=True, null=True)
    mobile_number_wife = models.CharField(verbose_name="Wife Mobile Number", max_length=255, blank=True, null=True)
    H_father_name = models.CharField(verbose_name="Husband Father Name", max_length=255, blank=True, null=True)
    H_mother_name = models.CharField(verbose_name="Husband Mother Name", max_length=255, blank=True, null=True)
    W_father_name = models.CharField(verbose_name="Wife Father Name", max_length=255, blank=True, null=True)
    W_mother_name = models.CharField(verbose_name="Wife Mother Name", max_length=255, blank=True, null=True)
    guardian_name = models.CharField(verbose_name="Guardian Name", max_length=255, blank=True, null=True)
    postal_address = models.CharField(verbose_name="Address", max_length=255, blank=True, null=True)
    residential_address = models.CharField(verbose_name="Residential Address", max_length=255, blank=True, null=True)
    date_of_marriage = models.DateField(verbose_name="Date of Marriage", blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.husband_name, self.wife_name)     


class Communion(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    mobile_number = models.CharField(verbose_name="Mobile Number", max_length=255, blank=True, null=True)
    dob = models.DateField(verbose_name="DoB", blank=True, null=True)
    date_of_communion = models.DateField(verbose_name="Date of Communion", blank=True, null=True)
    postal_address = models.CharField(verbose_name="Address", max_length=255, blank=True, null=True)
    residential_address = models.CharField(verbose_name="Residential Address", max_length=255, blank=True, null=True)

    def __str__(self):
        return (self.name)    

class StaffMember(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    category = models.CharField(verbose_name="Category", max_length=255)
    mobile_number = models.CharField(verbose_name="Mobile Number", max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    information = models.CharField(verbose_name="Information", max_length=255, blank=True, null=True)
    image = models.ImageField( upload_to='images/' ,blank=True, null=True, )

    def __str__(self):
        return (self.name)   

class ChurchActivity(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    date = models.DateField(verbose_name="date", max_length=255)
    group = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name)   

class Event(models.Model):
    event_name = models.CharField(verbose_name="Event Name", max_length=255)

    def __str__(self):
        return (self.event_name)  

class EventApplication(models.Model):
    name = models.ForeignKey(Account, on_delete=models.CASCADE,blank=True, null=True)
    event_name = models.CharField(verbose_name="Event Name", max_length=255)
    date_applied = models.DateTimeField(verbose_name="date applied", auto_now_add=True)
    description = models.CharField(verbose_name="Description", max_length=255, blank=True, null=True)
    application = models.CharField(verbose_name="application", max_length=255, blank=True, null=True)

    

