from django.contrib import admin

from .models import Profile, PhoneNumber, RequestDeleteUser, RecommendUser

admin.site.register(Profile)
admin.site.register(PhoneNumber)
admin.site.register(RequestDeleteUser)
admin.site.register(RecommendUser)
