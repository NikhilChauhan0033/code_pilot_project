from django.contrib import admin

# Register your models here.

# """
# PS C:\Users\admin\Desktop\Django\DjangoProject\code_pilot_project> python manage.py createsuperuser
# Username (leave blank to use 'admin'): admin
# Email address: admin123@gmail.com
# Password: admin
# Password (again): admin
# The password is too similar to the username.
# This password is too short. It must contain at least 8 characters.
# This password is too common.
# Bypass password validation and create user anyway? [y/N]: y
# Superuser created successfully.

# """

from .models import Course, Instructor, Cart, Checkout

admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Cart)
admin.site.register(Checkout)
