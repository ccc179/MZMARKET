from django.contrib import admin

from App.models import MainMustbuy, MainNav, MainShop,MainShow, MainWheel, FoodType, Goods, MZUser, Cart, ServerInfo


class UserAdmin(admin.ModelAdmin):
    list_display = 'u_username', 'u_roleid'
    search_fields = 'u_username',


'''账号tom 密码：门 '''
# 注册Model类
admin.site.register(MainShow)
admin.site.register(MainWheel)
admin.site.register(MainNav)
admin.site.register(MainMustbuy)
admin.site.register(MainShop)
admin.site.register(FoodType)
admin.site.register(Goods)
admin.site.register(MZUser, UserAdmin)
admin.site.register(Cart)
admin.site.register(ServerInfo)
