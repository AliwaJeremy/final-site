from import_export import resources
from .models import Attendance 

class AttendanceResource (resources.ModelResource):
    class meta:
        model = Attendance
