from django.contrib import admin
from employee.models import Employee,DailyLog,DailyLogAdditional,LogDateFlag

# Register your models here.


admin.site.register(Employee)
admin.site.register(DailyLog)
admin.site.register(DailyLogAdditional)
admin.site.register(LogDateFlag)



