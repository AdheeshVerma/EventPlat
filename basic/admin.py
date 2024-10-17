from django.contrib import admin
from .models import Profile,  Finish


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'clue_solved')
    
admin.site.register(Profile, ProfileAdmin)


# class CluesAdmin(admin.ModelAdmin):
#     list_display = ('location', 'clue', 'solved')
    
# admin.site.register(Clues, CluesAdmin)

class TimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'timeout')
    
admin.site.register(Finish, TimeAdmin)