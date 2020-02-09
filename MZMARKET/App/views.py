from django.http import HttpResponse
from django.shortcuts import render

from App.models import MainWheel, MainNav, MainMustbuy, MainShop, MainShow, FoodType, Goods


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustbuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shows = MainShow.objects.all()

    data = {
        "title": '萌猪商城',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shows': main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.all()

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    return render(request, 'main/cart.html', context={'title': '萌猪购物车'})


def mine(request):
    return render(request, 'main/mine.html', context={'title': '萌猪个人中心'})