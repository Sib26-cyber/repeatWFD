from django.contrib import admin
from .models import ReturnRequest,ReturnsStatus
from django.contrib.auth.models import User 


# Register your models here.
admin.site.register(ReturnRequest)
admin.site.register(ReturnsStatus)
