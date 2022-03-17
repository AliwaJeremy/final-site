from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from import_export.admin import ImportExportModelAdmin
from ackweb.models import *
from ackweb.forms import User
#from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm 
    model = User
    list_display = ['pk','email','first_name','last_name','membership_number', ]
    search_fields = ['email','username','id']
    readonly_fields = ['id', 'date_joined', 'last_login',]
    filter_horizontal  = ()
    list_filter = ['username']
    fieldsets = [
      (None, {'fields':('email','password','first_name', 'last_name', 'mobile_number','id','membership_number')}),
      ('Permissions', {'fields':('is_staff', ('is_active' , 'is_superuser'), )}),
      ('Advanced Options', {
        'classes':('collapse',),
        'fields':('groups','user_permissions')
      }),
      ('Additional Information', {'fields':('date_of_birth', 'address','title','gender','marital_status','church_status', 'department', 'cluster' , 'ministry' )}),
      ('Important Dates', {'fields':('date_joined', 'last_login' )}),
    ]
    


    # add_fieldsets= UserAdmin.add_fieldsets + (
      #   [None, {'fields':('email','username','first_name','last_name', 'mobile_number', 'date_of_birth','address','title','gender','marital_status','church_status','church_membership','cluster_number','talents',)}],
    # )
     #fieldsets = UserAdmin.fieldsets

admin.site.register(Account, CustomUserAdmin)
#admin.site.register(Department)
admin.site.register(Baptism)
admin.site.register(StaffMember)
admin.site.register(ChurchActivity)
admin.site.register(Event)
#admin.site.register(EventApplication)

@admin.register(Dependent)
class DependentAdmin(admin.ModelAdmin):
  list_display = ('id' , 'first_name' , 'last_name' , 'relationship', 'membership_number','parent1', 'parent2')
  search_fields = ('first_name' , 'last_name')

@admin.register(Attendance)
class ViewAdmin(ImportExportModelAdmin):
  list_display = ('name', 'id', 'date_of_attendance' , 'temperature' , 'mobile_number')
  ordering = ('date_of_attendance',)

@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
  ordering = ('date_applied',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  ordering = ('name',)

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
  ordering = ('name',)

@admin.register(Ministry)
class MinistrytAdmin(admin.ModelAdmin):
  ordering = ('name',)