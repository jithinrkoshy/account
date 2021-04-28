from django.contrib import admin
from product.models import ProductDailyLog,ProductDailyLogAdditional,ProductLogDateFlag

# Register your models here.


admin.site.register(ProductDailyLog)
admin.site.register(ProductDailyLogAdditional)
admin.site.register(ProductLogDateFlag)



