from django.contrib import admin

from App.models import MainMustbuy, MainNav, MainShop,MainShow, MainWheel
'''账号admin 密码a2316252221'''
# 注册Model类
admin.site.register(MainShow)
admin.site.register(MainWheel)
admin.site.register(MainNav)
admin.site.register(MainMustbuy)
admin.site.register(MainShop)