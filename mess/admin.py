from django.contrib import admin
from .models import *
from .models import AllowedStudent,Menu, Complaint, Attendance, Bill, Rating
admin.site.register(AllowedStudent)

admin.site.register(Menu)
admin.site.register(Complaint)
admin.site.register(Rating)
admin.site.register(Attendance)
admin.site.register(Bill)