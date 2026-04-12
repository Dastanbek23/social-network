from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comments)
